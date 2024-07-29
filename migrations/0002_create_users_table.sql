BEGIN;

DO
$do$
DECLARE
    current_migration_number integer := 2;
BEGIN
    IF NOT EXISTS (SELECT migration_number FROM migrations WHERE migration_number = current_migration_number) THEN

        -- Users Table
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            email TEXT NOT NULL,
            user_name TEXT NOT NULL,
            hashed_password TEXT NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            deleted_at TIMESTAMPTZ
        );

        CREATE UNIQUE INDEX users_email_deleted_at_unique_idx ON users (email, COALESCE(deleted_at, 'infinity'));

        INSERT INTO users(id, email, user_name, hashed_password) VALUES (1, 'bot@llm.ai', 'AI Bot', '$2b$12$bDi4IGlET/2IhBBhebE5f.4sHLAPaihnXvMJZ8ujcXi6W3s.PTi4O');
        INSERT INTO users(id, email, user_name, hashed_password) VALUES (2, 'ramish@test.com', 'Ramish', '$2b$12$bDi4IGlET/2IhBBhebE5f.4sHLAPaihnXvMJZ8ujcXi6W3s.PTi4O');


        INSERT INTO migrations(migration_number) VALUES (current_migration_number);
    ELSE
        RAISE NOTICE 'Already ran migration %.', current_migration_number;
    END IF;
END
$do$;

COMMIT;
