#!/bin/bash
set -e  # exit immediately if any command fails

echo "Creating application user and database..."

# Using psql as the postgres superuser (which init-db.sh runs as by default)
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL

    -- Create user only if it doesn't exist (replaces your COUNT(*) check)
    DO \$\$
    BEGIN
        IF NOT EXISTS (
            SELECT FROM pg_catalog.pg_roles WHERE rolname = '$APP_DB_USER'
        ) THEN
            CREATE ROLE "$APP_DB_USER" LOGIN PASSWORD '$APP_DB_PASSWORD';
            RAISE NOTICE 'User % created.', '$APP_DB_USER';
        ELSE
            RAISE NOTICE 'User % already exists, skipping.', '$APP_DB_USER';
        END IF;
    END
    \$\$;

    -- Grant access to the database
    GRANT ALL PRIVILEGES ON DATABASE "$POSTGRES_DB" TO "$APP_DB_USER";

    -- Grant schema access
    GRANT ALL ON SCHEMA public TO "$APP_DB_USER";

    -- Grant access on existing tables
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "$APP_DB_USER";

    -- Grant access on future tables automatically
    ALTER DEFAULT PRIVILEGES IN SCHEMA public
        GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO "$APP_DB_USER";

EOSQL

echo "Database setup complete."