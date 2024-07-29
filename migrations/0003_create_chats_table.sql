BEGIN;

DO
$do$
DECLARE
    current_migration_number integer := 3;
BEGIN
    IF NOT EXISTS (SELECT migration_number FROM migrations WHERE migration_number = current_migration_number) THEN

        CREATE TABLE chats (
            id SERIAL PRIMARY KEY,
            chat_name TEXT NOT NULL,
            user_id INTEGER NOT NULL REFERENCES users(id),
            created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            deleted_at TIMESTAMPTZ
        );

        CREATE UNIQUE INDEX chats_name_user_id_deleted_at_unique_idx ON chats (chat_name, user_id, COALESCE(deleted_at, 'infinity'));

        INSERT INTO migrations(migration_number) VALUES (current_migration_number);
    ELSE
        RAISE NOTICE 'Already ran migration %.', current_migration_number;
    END IF;
END
$do$;

COMMIT;
