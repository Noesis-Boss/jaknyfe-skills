ALTER TABLE messages ADD COLUMN next_attempt_at TEXT;
ALTER TABLE messages ADD COLUMN lease_owner TEXT;
ALTER TABLE messages ADD COLUMN lease_until TEXT;
CREATE INDEX IF NOT EXISTS idx_messages_queue ON messages(status, next_attempt_at, lease_until, created_at);
