from pathlib import Path
from typing import Any

import psycopg2
from alembic import command, script, util
from alembic.config import Config
from alembic.runtime import migration
from psycopg2 import sql

from app.core.config import BASE_DIR, settings
from app.db.session import engine


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
    query = "SELECT COUNT(*) FROM pg_catalog.pg_roles WHERE rolname = %s"
    cur.execute(query, (settings.DB_USER,))
    user_exists: Any = cur.fetchone()
    if user_exists == 0:
        query: sql.Composed = sql.SQL("CREATE ROLE {0} LOGIN PASSWORD {1}").format(
            sql.Identifier(settings.DB_USER),
            sql.Literal(settings.DB_PASSWORD),
        )
        cur.execute(query.as_string(con))
        print("User Created.")
        print("Granting privileges on database to user.")
        grant_db = "GRANT ALL PRIVILEGES ON DATABASE %s to %s;"
        cur.execute(grant_db, (db_name, settings.DB_USER))
        grant_schema = "GRANT ALL ON SCHEMA public TO %s;"
        cur.execute(grant_schema, (settings.DB_USER,))
        grant_tables = "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO %s;"
        cur.execute(grant_tables, (settings.DB_USER,))
        alter_schema_privilege = "ALTER DEFAULT PRIVILEGES FOR USER %s IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO %s;"
        cur.execute(alter_schema_privilege, (settings.DB_USER, settings.DB_USER))
        con.commit()
        print(f"Granted privileges on database {db_name} to user.")
    else:
        print("User already exists.")


def db_creation(con) -> tuple[str, bool]:
    con.autocommit = True
    cur: Any = con.cursor()
    query = "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s"
    cur.execute(query, (settings.DB_NAME,))
    db_exists: Any = cur.fetchone()
    if not db_exists:
        cur.execute(f"CREATE DATABASE {settings.DB_NAME};")
        print("Database created.")
    else:
        print("Database already exists.")
    con.commit()
    return settings.DB_NAME, bool(db_exists)


def run_migrations() -> None:
    try:
        alembic_init_path: Path = BASE_DIR / "alembic.ini"
        alembic_cfg = Config(alembic_init_path)
        alembic_cfg.set_section_option("logger_alembic", "level", "ERROR")
        alembic_cfg.attributes["configure_logger"] = False
        command.revision(alembic_cfg, autogenerate=True)
        conn: migration.Connection = engine.connect()
        script_: command.ScriptDirectory = script.ScriptDirectory.from_config(
            alembic_cfg,
        )
        context: migration.MigrationContext = migration.MigrationContext.configure(conn)
        script_head: str | None = script_.get_current_head()
        context_head: str | None = context.get_current_revision()
        print("script_head", script_head)
        print("context_head", context_head)
        if context.get_current_revision() != script_.get_current_head():
            print("The database is not up-to-date. Upgrading the database.")
            command.upgrade(alembic_cfg, "head")
        else:
            print("The database is up-to-date. No need to run migrations.")
    except util.exc.CommandError:
        command.stamp(alembic_cfg, "head")
        print(f"Migration failed ! revert head to {context_head}")
    finally:
        print("Running finally block.")


if __name__ == "__main__":
    print("Running it as a script.")
