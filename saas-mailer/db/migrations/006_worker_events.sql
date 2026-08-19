ALTER TABLE messages ADD COLUMN subject TEXT NOT NULL DEFAULT '';
ALTER TABLE messages ADD COLUMN body TEXT NOT NULL DEFAULT '';
ALTER TABLE messages ADD COLUMN attempt_count INTEGER NOT NULL DEFAULT 1;
ALTER TABLE messages ADD COLUMN error_code TEXT;
CREATE INDEX IF NOT EXISTS idx_messages_idempotency_key ON messages(idempotency_key);
