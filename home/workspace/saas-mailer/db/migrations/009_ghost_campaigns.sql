ALTER TABLE campaigns ADD COLUMN campaign_type TEXT NOT NULL DEFAULT 'sequence' CHECK (campaign_type IN ('newsletter', 'sequence'));
ALTER TABLE campaigns ADD COLUMN preview_text TEXT NOT NULL DEFAULT '';
ALTER TABLE campaigns ADD COLUMN template TEXT NOT NULL DEFAULT 'plain';
ALTER TABLE campaigns ADD COLUMN scheduled_at TEXT;

CREATE TABLE IF NOT EXISTS subscriber_preferences (
  organization_id TEXT NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  contact_id TEXT NOT NULL,
  topic TEXT NOT NULL DEFAULT 'general',
  status TEXT NOT NULL DEFAULT 'subscribed' CHECK (status IN ('subscribed', 'paused', 'unsubscribed')),
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (organization_id, contact_id, topic),
  FOREIGN KEY (organization_id, contact_id) REFERENCES contacts(organization_id, id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_subscriber_preferences_contact ON subscriber_preferences(organization_id, contact_id);
