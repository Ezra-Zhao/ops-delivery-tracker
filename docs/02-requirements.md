# Requirements List

> SYNTHETIC / SIMULATED demo. Requirement IDs are for traceability inside
> this repository only.

## Functional requirements

| ID | Requirement | Implemented in | Verified by |
|---|---|---|---|
| FR-1 | Track sites with an ownership flag distinguishing first-party (1P) and third-party (3P) capacity in one portfolio model | odt/schema.sql (site) | test_model.py |
| FR-2 | Track milestones with baseline, forecast, and due dates, status, owner, and last-updated timestamp | odt/schema.sql (milestone) | test_model.py, test_stale.py |
| FR-3 | Automatically flag a milestone stale/red when it is not completed and has had no update for more than a configurable number of days (default 7) | odt/portfolio.py | test_stale.py |
| FR-4 | Maintain risk and decision registers as first-class entities linked to sites (exposure score, owner, mitigation, decision date; options, decider, rationale) | odt/schema.sql (risk, decision) | test_model.py |
| FR-5 | Handover sign-off follows a state machine: evidence submission, review, sign-off; sign-off is blocked without the full evidence pack and while a severity blocker is open | odt/handover.py | test_handover.py |
| FR-6 | Exceptions (waivers) follow an explicit path with a mandatory expiry and a recorded decider; both approval and rejection return the handover to review with the record kept | odt/handover.py | test_handover.py |
| FR-7 | After sign-off, post-handover actions can be opened, tracked, and completed | odt/handover.py | test_handover.py |
| FR-8 | Controlled documents are registered with version, owner, and approval status; a new version must name what it supersedes; superseded versions are retired with an obsolescence flag and reason | odt/governance.py | test_governance.py |
| FR-9 | SLA attainment and MTTR are computed from ticket timestamps and per-priority SLA targets by named SQL queries | sql/queries.sql, odt/reporting.py | test_reporting.py |
| FR-10 | Milestone achievement is computed over milestones due to date | sql/queries.sql | test_reporting.py |
| FR-11 | A one-page executive weekly report is generated from the queries, conclusion first, with stale milestones named as watch items | odt/reporting.py, scripts/generate_report.py | VERIFICATION.md cross-check |

## Non-functional requirements

| ID | Requirement | How this demo meets it |
|---|---|---|
| NFR-1 | Reproducibility: any reported number can be re-derived from the seeded database with the published queries | Deterministic seed (odt/seed.py, fixed timestamps); VERIFICATION.md cross-checks report vs raw SQL |
| NFR-2 | No external services or credentials required to run | Python 3.12 standard library only (sqlite3); pytest is the only dev dependency |
| NFR-3 | Honest labeling: synthetic data is declared at every entry point | README first screen, report header, seed module docstring |
| NFR-4 | Small, auditable codebase: workflow rules live in code with tests, not in prose alone | State machine and governance rules are enforced by exceptions, with negative-path tests |

## Out of scope for this demo (stated, not hidden)

- Authentication, role-based access control, and audit logging.
- Any real integration with a ticketing or reporting product (interfaces in
  03-integration-diagram.md are design assumptions only).
- Notifications, scheduling, and multi-user concurrency.
