"""Deterministic synthetic seed. Reference as_of date: 2026-11-02.
Counts by construction:
  sites 3 (2x 1P, 1x 3P); milestones 12 (10 due by 2026-11-02, 8 completed);
  risks 6; decisions 5; tickets 20 (16 resolved, 4 open).
Ticket durations are fixed timestamps, so SLA / MTTR are fully reproducible.
"""
AS_OF = "2026-11-02"

SITES = [
    (1, "SITE-A", "North Ridge Compute Hall", "1P", None, "us-west", "active"),
    (2, "SITE-B", "Harbor Point Compute Hall", "1P", None, "us-west", "active"),
    (3, "SITE-C", "Partner Colo East", "3P", "Synthetic Partner LLC", "us-east", "active"),
]

# id, site, name, baseline, forecast, due, status, pct, owner, updated_at
MILESTONES = [
    (1, 1, "Capacity acceptance - Hall A", "2026-09-15", "2026-09-15", "2026-09-15", "completed", 100, "ops-lead-a", "2026-09-15"),
    (2, 1, "Network fabric turn-up", "2026-09-30", "2026-09-30", "2026-09-30", "completed", 100, "net-lead", "2026-09-30"),
    (3, 1, "Ops handover - Hall A", "2026-10-10", "2026-10-12", "2026-10-10", "completed", 100, "tpm-demo", "2026-10-12"),
    (4, 1, "Monitoring integration live", "2026-10-20", "2026-10-20", "2026-10-20", "completed", 100, "tooling-lead", "2026-10-20"),
    (5, 2, "Capacity acceptance - Hall B", "2026-10-05", "2026-10-05", "2026-10-05", "completed", 100, "ops-lead-b", "2026-10-05"),
    (6, 2, "Ticketing workflow cutover", "2026-10-18", "2026-10-18", "2026-10-18", "completed", 100, "tooling-lead", "2026-10-18"),
    (7, 2, "Ops handover - Hall B", "2026-10-28", "2026-10-28", "2026-10-28", "completed", 100, "tpm-demo", "2026-10-28"),
    (8, 3, "Partner capacity acceptance", "2026-10-15", "2026-10-15", "2026-10-15", "completed", 100, "partner-mgr", "2026-10-15"),
    (9, 3, "Partner SLA reporting live", "2026-10-25", "2026-11-05", "2026-10-25", "in_progress", 60, "partner-mgr", "2026-10-20"),
    (10, 1, "Runbook library v1 published", "2026-10-30", "2026-11-06", "2026-10-30", "in_progress", 40, "docs-owner", "2026-10-22"),
    (11, 2, "Capacity expansion forecast Q1", "2026-11-20", "2026-11-20", "2026-11-20", "in_progress", 30, "capacity-planner", "2026-11-01"),
    (12, 3, "Partner handover - Phase 2", "2026-11-25", "2026-11-25", "2026-11-25", "not_started", 0, "partner-mgr", "2026-10-30"),
]
# Stale check at as_of=2026-11-02, threshold 7d, not completed:
#   #9 updated 2026-10-20 -> 13 days stale; #10 updated 2026-10-22 -> 11 days stale;
#   #11 updated 2026-11-01 -> 1 day current; #12 updated 2026-10-30 -> 3 days current.
# Expected stale set = {9, 10}.

RISKS = [
    (1, 1, "Utility feed B commissioning slip", "utility", 3, 4, "high", "ops-lead-a", "Weekly utility sync; expedite witness test", "open", "2026-11-10"),
    (2, 2, "Ticketing cutover data quality", "tooling", 2, 3, "medium", "tooling-lead", "Dual-run old and new queues for 2 weeks", "open", "2026-11-08"),
    (3, 3, "Partner report format mismatch", "partner", 4, 3, "high", "partner-mgr", "Agree report schema; weekly sample exchange", "open", "2026-11-06"),
    (4, 1, "Runbook owner bandwidth", "staffing", 3, 2, "medium", "docs-owner", "Split library by system; two backup owners", "open", "2026-11-12"),
    (5, 2, "Spare parts lead time", "supply", 2, 4, "medium", "ops-lead-b", "Raise min stock for two critical SKUs", "mitigated", "2026-10-30"),
    (6, 3, "Partner escalation path untested", "partner", 2, 3, "low", "partner-mgr", "Run one tabletop escalation drill", "open", "2026-11-15"),
]

DECISIONS = [
    (1, 1, "Adopt single delivery tracker for 1P and 3P sites", "Two trackers vs one tracker", "One tracker, ownership flag separates 1P/3P", "tpm-demo", "One roll-up for executive reporting; 3P access scoped by site", "2026-09-20", "decided"),
    (2, 2, "Ticketing cutover timing", "Big-bang vs phased", "Phased by hall", "ops-lead-b", "Limits blast radius during acceptance window", "2026-10-01", "decided"),
    (3, 3, "Partner SLA report cadence", "Monthly vs weekly", "Weekly", "partner-mgr", "Weekly cadence surfaces format drift early", "2026-10-12", "decided"),
    (4, 1, "Stale threshold for milestones", "7 vs 14 days", "7 days without update flags stale", "tpm-demo", "Weekly governance rhythm makes 7 days the natural tripwire", "2026-09-25", "decided"),
    (5, 2, "Handover evidence pack contents", "Free-form vs fixed pack", "Fixed pack: test report, checklist, ops readiness note", "tpm-demo", "Mirrors gate evidence discipline: sign-off needs attached evidence", "2026-10-03", "decided"),
]

# id, site, title, priority, sla_hours, status, created_at, resolved_at, category
TICKETS = [
    (1, 1, "P1 network flap Hall A", "P1", 4, "resolved", "2026-10-20 08:00", "2026-10-20 10:00", "network"),
    (2, 1, "P1 power alarm Hall A", "P1", 4, "resolved", "2026-10-22 09:00", "2026-10-22 14:00", "power"),
    (3, 2, "P1 fabric outage Hall B", "P1", 4, "resolved", "2026-10-24 10:00", "2026-10-24 13:00", "network"),
    (4, 3, "P1 partner link down", "P1", 4, "resolved", "2026-10-26 07:00", "2026-10-26 09:30", "partner"),
    (5, 1, "P2 monitoring gap", "P2", 24, "resolved", "2026-10-20 08:00", "2026-10-21 04:00", "tooling"),
    (6, 1, "P2 runbook access issue", "P2", 24, "resolved", "2026-10-21 09:00", "2026-10-22 15:00", "access"),
    (7, 2, "P2 ticket routing error", "P2", 24, "resolved", "2026-10-23 11:00", "2026-10-23 23:00", "tooling"),
    (8, 2, "P2 cooling sensor drift", "P2", 24, "resolved", "2026-10-25 06:00", "2026-10-26 02:00", "cooling"),
    (9, 3, "P2 partner report delay", "P2", 24, "resolved", "2026-10-27 08:00", "2026-10-28 20:00", "partner"),
    (10, 1, "P2 backup job failure", "P2", 24, "resolved", "2026-10-28 10:00", "2026-10-28 22:00", "systems"),
    (11, 1, "P3 doc link cleanup", "P3", 72, "resolved", "2026-10-20 09:00", "2026-10-21 09:00", "docs"),
    (12, 2, "P3 label mismatch", "P3", 72, "resolved", "2026-10-22 09:00", "2026-10-25 09:00", "docs"),
    (13, 2, "P3 dashboard typo", "P3", 72, "resolved", "2026-10-24 09:00", "2026-10-25 21:00", "tooling"),
    (14, 3, "P3 partner contact update", "P3", 72, "resolved", "2026-10-26 09:00", "2026-10-27 09:00", "partner"),
    (15, 1, "P3 archive old alerts", "P3", 72, "resolved", "2026-10-27 09:00", "2026-10-31 09:00", "systems"),
    (16, 3, "P3 report template fix", "P3", 72, "resolved", "2026-10-28 09:00", "2026-10-29 09:00", "partner"),
    (17, 1, "P2 open investigation cooling", "P2", 24, "open", "2026-11-01 08:00", None, "cooling"),
    (18, 2, "P3 open doc review", "P3", 72, "open", "2026-11-01 10:00", None, "docs"),
    (19, 3, "P2 open partner metric gap", "P2", 24, "open", "2026-11-02 07:00", None, "partner"),
    (20, 1, "P3 open training record sync", "P3", 72, "open", "2026-11-02 08:00", None, "training"),
]
# Hand-computed expectations (verified by tests against SQL, not assumed):
# Resolved durations h: 2,5,3,2.5 | 20,30,12,20,36,12 | 24,72,36,24,96,24
# SLA met (duration <= sla_hours): P1: 2,3,2.5 met; 5 missed -> 3/4
#   P2: 20,12,20,12 met; 30,36 missed -> 4/6 ; P3: 24,72,36,24,24 met; 96 missed -> 5/6
#   (ticket 12 duration is exactly 72h, equal to its SLA, so it counts as met)
#   Total met = 12 of 16 -> 75.0%
# MTTR = sum durations / 16 = 418.5 / 16 = 26.15625 -> 26.16 hours

DOCUMENTS = [
    # doc_code, title, owner -- v1 approved then obsoleted by v2 (seeded via governance API in seed_db)
    ("OPS-RBK-001", "Operations Runbook - Hall A", "docs-owner"),
    ("OPS-HOV-002", "Handover Evidence Pack Template", "tpm-demo"),
    ("OPS-GOV-003", "Controlled Document Procedure", "tpm-demo"),
]

def seed_db(conn):
    conn.executemany("INSERT INTO site VALUES (?,?,?,?,?,?,?)", SITES)
    conn.executemany("INSERT INTO milestone VALUES (?,?,?,?,?,?,?,?,?,?)", MILESTONES)
    conn.executemany("INSERT INTO risk VALUES (?,?,?,?,?,?,?,?,?,?,?)", RISKS)
    conn.executemany("INSERT INTO decision VALUES (?,?,?,?,?,?,?,?,?)", DECISIONS)
    conn.executemany("INSERT INTO ticket VALUES (?,?,?,?,?,?,?,?,?)", TICKETS)
    conn.commit()
    # Documents are seeded through the governance API so the lifecycle is real:
    # OPS-RBK-001 v1 approved -> v2 registered (supersedes v1) -> v2 approved -> v1 obsolete.
    from odt.governance import register_document, submit_for_review, approve_document, mark_obsolete
    v1, _ = register_document(conn, "OPS-RBK-001", "Operations Runbook - Hall A", "docs-owner", "2026-09-01")
    submit_for_review(conn, v1); approve_document(conn, v1, "tpm-demo")
    v2, _ = register_document(conn, "OPS-RBK-001", "Operations Runbook - Hall A", "docs-owner", "2026-10-15", supersedes_id=v1)
    submit_for_review(conn, v2); approve_document(conn, v2, "tpm-demo")
    mark_obsolete(conn, v1, "Superseded by version 2 on 2026-10-15")
    d2, _ = register_document(conn, "OPS-HOV-002", "Handover Evidence Pack Template", "tpm-demo", "2026-10-03")
    submit_for_review(conn, d2); approve_document(conn, d2, "ops-lead-a")
    d3, _ = register_document(conn, "OPS-GOV-003", "Controlled Document Procedure", "tpm-demo", "2026-10-05")
    return conn
