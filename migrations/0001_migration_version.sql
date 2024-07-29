BEGIN;

    CREATE TABLE migrations (
        id SERIAL PRIMARY KEY,
        migration_number int NOT NULL UNIQUE,
        created_at timestamp default current_timestamp
    );

    INSERT INTO migrations(migration_number)
    VALUES (1);

COMMIT;
