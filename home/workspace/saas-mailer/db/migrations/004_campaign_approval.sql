ALTER TABLE campaigns ADD COLUMN approved_at TEXT;
ALTER TABLE campaigns ADD COLUMN approved_by TEXT;
ALTER TABLE campaigns ADD COLUMN sending_account_id TEXT;
ALTER TABLE campaigns ADD COLUMN sending_window_start TEXT;
ALTER TABLE campaigns ADD COLUMN sending_window_end TEXT;
ALTER TABLE campaigns ADD COLUMN daily_send_limit INTEGER NOT NULL DEFAULT 100;
