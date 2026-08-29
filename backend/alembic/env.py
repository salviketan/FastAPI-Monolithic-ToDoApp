import sys
from pathlib import Path

# Add app directory to path so modules can be imported
sys.path.append(str(Path(__file__).resolve().parents[1]))

import asyncio
from logging.config import fileConfig
from typing import Any

from alembic import context
from app.core.config import settings
from app.db.base import Base
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Connection
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config: context.Config = context.config

# Get the rendered URL string with percent-encoding
db_url: str = settings.SQLALCHEMY_DB_URL.render_as_string(hide_password=False)

# Escape % to %% specifically for ConfigParser / Alembic
safe_db_url: str = db_url.replace("%", "%%")

# Set option safely
config.set_main_option("sqlalchemy.url", safe_db_url)


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None and config.attributes.get(
    "configure_logger",
    True,
):
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

target_metadata: Any = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def include_object(object, name, type_, reflected, compare_to) -> bool:
    if type_ == "table" and reflected and compare_to is None:
        return False

    # # Dynamic Schema Allow-List:
    # # If a schema is specified during reflection, ensure it belongs to your target database/models
    # if object.schema:
    #     # Get target schema from your settings, or extract valid schemas from target_metadata
    #     target_schemas = {target_metadata.schema, settings.POSTGRES_DB}
    #     if object.schema not in target_schemas:
    #         return False

    return True


def process_revision_directives(context, revision, directives) -> None:
    script: Any = directives[0]
    if script.upgrade_ops.is_empty():
        directives[:] = []


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url: Any = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # Prevents Alembic from scanning system schemas
        include_schemas=False,  # Changed to "True" - If you ever need multi-schema support in future
        include_object=include_object,
        compare_type=True,
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


###### For async drives #####
def do_run_migrations(connection: Connection) -> None:
    """Helper method executed inside the greenlet runner."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        # Prevents Alembic from scanning system schemas
        include_schemas=False,  # Changed to "True" - If you ever need multi-schema support in future
        include_object=include_object,
        process_revision_directives=process_revision_directives,
        compare_type=True,
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In 'online' mode, create an AsyncEngine and execute migrations in a greenlet context."""
    # Create engine directly to inject asyncmy connection parameters
    connectable: AsyncEngine = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # run_sync wraps the sync migration runner inside greenlet to support async drivers
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


###### For async drives ends #####


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    # For async drivers
    asyncio.run(run_async_migrations())

    # # -------------------------------------------------------------
    # # UNUSED: Synchronous driver bolck (Kept for reference)
    # # -------------------------------------------------------------
    # connectable: Engine = engine_from_config(
    #     config.get_section(config.config_ini_section, {}),
    #     prefix="sqlalchemy.",
    #     poolclass=pool.NullPool,
    # )

    # with connectable.connect() as connection:
    #     context.configure(
    #         connection=connection,
    #         target_metadata=target_metadata,
    #         # Prevents Alembic from scanning system schemas
    #         include_schemas=False,  # Changed to "True" - If you ever need multi-schema support in future
    #         include_object=include_object,
    #         process_revision_directives=process_revision_directives,
    #         compare_type=True,
    #         render_as_batch=True,
    #     )

    #     with context.begin_transaction():
    #         context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
