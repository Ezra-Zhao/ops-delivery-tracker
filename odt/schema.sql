-- ops-delivery-tracker schema (SQLite, Python stdlib sqlite3)
-- All data seeded into this schema is SYNTHETIC / SIMULATED.
CREATE TABLE IF NOT EXISTS site (
  id INTEGER PRIMARY KEY,
  code TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  ownership TEXT NOT NULL CHECK (ownership IN ('1P','3P')),
  partner_name TEXT,
  region TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'active'
);
CREATE TABLE IF NOT EXISTS milestone (
  id INTEGER PRIMARY KEY,
  site_id INTEGER NOT NULL REFERENCES site(id),
  name TEXT NOT NULL,
  baseline_date TEXT NOT NULL,
  forecast_date TEXT NOT NULL,
  due_date TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('not_started','in_progress','completed','blocked')),
  percent_complete INTEGER NOT NULL DEFAULT 0,
  owner TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS risk (
  id INTEGER PRIMARY KEY,
  site_id INTEGER NOT NULL REFERENCES site(id),
  title TEXT NOT NULL,
  category TEXT NOT NULL,
  probability INTEGER NOT NULL CHECK (probability BETWEEN 1 AND 5),
  impact INTEGER NOT NULL CHECK (impact BETWEEN 1 AND 5),
  severity TEXT NOT NULL DEFAULT '',
  owner TEXT NOT NULL,
  mitigation TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'open',
  decision_date TEXT
);
CREATE TABLE IF NOT EXISTS decision (
  id INTEGER PRIMARY KEY,
  site_id INTEGER REFERENCES site(id),
  title TEXT NOT NULL,
  options_considered TEXT NOT NULL,
  decided TEXT NOT NULL,
  decider TEXT NOT NULL,
  rationale TEXT NOT NULL,
  decided_on TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'decided'
);
CREATE TABLE IF NOT EXISTS ticket (
  id INTEGER PRIMARY KEY,
  site_id INTEGER NOT NULL REFERENCES site(id),
  title TEXT NOT NULL,
  priority TEXT NOT NULL CHECK (priority IN ('P1','P2','P3')),
  sla_hours REAL NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('open','resolved','closed')),
  created_at TEXT NOT NULL,
  resolved_at TEXT,
  category TEXT NOT NULL DEFAULT 'operations'
);
CREATE TABLE IF NOT EXISTS handover (
  id INTEGER PRIMARY KEY,
  site_id INTEGER NOT NULL REFERENCES site(id),
  title TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  exception_reason TEXT,
  exception_expiry TEXT,
  exception_decider TEXT,
  created_at TEXT NOT NULL,
  signed_off_by TEXT,
  signed_off_at TEXT
);
CREATE TABLE IF NOT EXISTS handover_evidence (
  id INTEGER PRIMARY KEY,
  handover_id INTEGER NOT NULL REFERENCES handover(id),
  evidence_type TEXT NOT NULL,
  title TEXT NOT NULL,
  reference TEXT NOT NULL,
  submitted_by TEXT NOT NULL,
  submitted_at TEXT NOT NULL,
  accepted INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS post_handover_action (
  id INTEGER PRIMARY KEY,
  handover_id INTEGER NOT NULL REFERENCES handover(id),
  title TEXT NOT NULL,
  owner TEXT NOT NULL,
  due_date TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open','done','overdue'))
);
CREATE TABLE IF NOT EXISTS controlled_document (
  id INTEGER PRIMARY KEY,
  doc_code TEXT NOT NULL,
  title TEXT NOT NULL,
  version INTEGER NOT NULL,
  owner TEXT NOT NULL,
  approval_status TEXT NOT NULL DEFAULT 'draft'
    CHECK (approval_status IN ('draft','in_review','approved','rejected')),
  is_obsolete INTEGER NOT NULL DEFAULT 0,
  obsolete_reason TEXT,
  supersedes_id INTEGER REFERENCES controlled_document(id),
  created_at TEXT NOT NULL,
  approved_by TEXT,
  UNIQUE (doc_code, version)
);
