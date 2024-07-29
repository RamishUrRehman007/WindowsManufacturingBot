BEGIN;

DO
$do$
DECLARE
    current_migration_number integer := 9;
BEGIN
    IF NOT EXISTS (SELECT migration_number FROM migrations WHERE migration_number = current_migration_number) THEN

        -- Messages Table
        CREATE TABLE messages (
            id SERIAL PRIMARY KEY,
            chat_id INTEGER NOT NULL REFERENCES chats(id),
            user_id INTEGER NOT NULL REFERENCES users(id),
            message TEXT NOT NULL,
            message_status TEXT NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        INSERT INTO migrations(migration_number) VALUES (current_migration_number);
    ELSE
        RAISE NOTICE 'Already ran migration %.', current_migration_number;
    END IF;
END
$do$;

COMMIT;
