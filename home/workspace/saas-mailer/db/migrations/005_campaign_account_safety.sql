PRAGMA foreign_keys = OFF;
ALTER TABLE sending_accounts ADD COLUMN daily_send_limit INTEGER NOT NULL DEFAULT 100;
ALTER TABLE sending_accounts ADD COLUMN timezone TEXT NOT NULL DEFAULT 'UTC';
CREATE TABLE campaigns_new (
  id TEXT PRIMARY KEY, organization_id TEXT NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  name TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'draft', created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  approved_at TEXT, approved_by TEXT, sending_account_id TEXT, sending_window_start TEXT, sending_window_end TEXT,
  daily_send_limit INTEGER NOT NULL DEFAULT 100, timezone TEXT NOT NULL DEFAULT 'UTC', UNIQUE (organization_id, id),
  FOREIGN KEY (organization_id, sending_account_id) REFERENCES sending_accounts(organization_id, id) ON DELETE RESTRICT
);
INSERT INTO campaigns_new (id, organization_id, name, status, created_at, approved_at, approved_by, sending_account_id, sending_window_start, sending_window_end, daily_send_limit)
SELECT id, organization_id, name, status, created_at, approved_at, approved_by, sending_account_id, sending_window_start, sending_window_end, daily_send_limit FROM campaigns;
DROP TABLE campaigns;
ALTER TABLE campaigns_new RENAME TO campaigns;
CREATE INDEX IF NOT EXISTS idx_campaigns_organization_id ON campaigns(organization_id);
PRAGMA foreign_keys = ON;
