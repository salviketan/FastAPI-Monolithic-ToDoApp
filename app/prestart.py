from pathlib import Path
from typing import Any

import psycopg2
from alembic import command, script
from alembic.config import Config
from alembic.runtime import migration
from core.config import BASE_DIR, settings
from db.session import engine
from psycopg2 import sql


def db_connection(*, dbname: bool = False) -> psycopg2.connection:
    if dbname:
        con = psycopg2.connect(
            user=settings.ROOT_DB_USER,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            password=settings.ROOT_DB_PASSWORD,
            database=settings.DB_NAME,
        )
        return con
    con: psycopg2.connection = psycopg2.connect(
        user=settings.ROOT_DB_USER,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        password=settings.ROOT_DB_PASSWORD,
    )
    return con


def user_creation(con, db_name: str) -> None:
    cur: Any = con.cursor()
    query = "SELECT COUNT(*) FROM pg_catalog.pg_roles WHERE rolname = %s;"
    print("--" * 10, cur.execute(query, (settings.DB_USER,)))
    cur.execute(query, (settings.DB_USER,))
    user_exists: Any = cur.fetchone()[0]
    print("--" * 10, user_exists)
    if user_exists == 0:
        query: sql.Composed = sql.SQL("CREATE ROLE {0} LOGIN PASSWORD {1};").format(
            sql.Identifier(settings.DB_USER),
            sql.Literal(settings.DB_PASSWORD),
        )
        cur.execute(query.as_string(con))
        print("User Created.")
        print("Granting privileges on database to user.")
        grant_db: sql.Composed = sql.SQL(
            "GRANT ALL PRIVILEGES ON DATABASE {0} to {1};",
        ).format(
            sql.Identifier(db_name),
            sql.Identifier(settings.DB_USER),
        )
        cur.execute(grant_db.as_string(con))
        grant_schema: sql.Composed = sql.SQL(
            "GRANT ALL ON SCHEMA public TO {0};",
        ).format(
            sql.Identifier(settings.DB_USER),
        )
        cur.execute(grant_schema.as_string(con))
        grant_tables: sql.Composed = sql.SQL(
            "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO {0};",
        ).format(
            sql.Identifier(settings.DB_USER),
        )
        cur.execute(grant_tables.as_string(con))
        alter_schema_privilege: sql.Composed = sql.SQL(
            "ALTER DEFAULT PRIVILEGES FOR USER {0} IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO {1};",
        ).format(
            sql.Identifier(settings.DB_USER),
            sql.Identifier(settings.DB_USER),
        )
        cur.execute(alter_schema_privilege.as_string(con))
        con.commit()
        print(f"Granted privileges on database {db_name} to user.")
    else:
        print("User already exists.")


def db_creation(con) -> tuple[str, bool]:
    con.autocommit = True
    cur: Any = con.cursor()
    query = "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s;"
    cur.execute(query, (settings.DB_NAME,))
    db_exists: Any = cur.fetchone()
    if not db_exists:
        cur.execute(
            sql.SQL("CREATE DATABASE {0};")
            .format(
                sql.Identifier(settings.DB_NAME),
            )
            .as_string(con),
        )
        print("Database created.")
    else:
        print("Database already exists.")
    con.commit()
    return settings.DB_NAME, bool(db_exists)


def run_migrations() -> None:
    alembic_init_path: Path = BASE_DIR / "alembic.ini"
    alembic_cfg = Config(alembic_init_path)

    # Use a single connection for all checks to ensure consistency
    with engine.begin() as conn:
        alembic_cfg.attributes["connection"] = conn

        script_dir: command.ScriptDirectory = script.ScriptDirectory.from_config(
            alembic_cfg,
        )
        context: migration.MigrationContext = migration.MigrationContext.configure(conn)

        current_rev: str | None = context.get_current_revision()
        head_rev: str | None = script_dir.get_current_head()

        print(f"Current DB revision: {current_rev}")
        print(f"Latest script revision: {head_rev}")

        if current_rev != head_rev:
            print("Upgrading database to head...")
            command.upgrade(alembic_cfg, "head")
        else:
            print("Database is already at head.")


if __name__ == "__main__":
    print("Running it as a script.")
