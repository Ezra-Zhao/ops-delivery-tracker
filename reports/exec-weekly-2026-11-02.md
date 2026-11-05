# Executive Weekly Report - Operations Delivery Portfolio (week ending 2026-11-02)

> SYNTHETIC / SIMULATED DATA - generated from the seeded demo database. Not a real portfolio.

## Bottom line first

Portfolio needs attention: at least one headline metric is below its target line (SLA 85%, milestone achievement 80%).
- SLA attainment: 75.0% (12 of 16 resolved tickets met SLA).
- MTTR: 26.16 hours across 16 resolved tickets.
- Milestone achievement (due to date): 80.0% (8 of 10 due milestones completed).
- Open tickets: 4 of 20 total. Stale milestones (no update in over 7 days, not completed): 2.
- Open risks by severity: medium: 2, high: 2, low: 1.

## MTTR by priority (hours)

| Priority | Resolved | MTTR hours |
|---|---|---|
| P1 | 4 | 3.13 |
| P2 | 6 | 21.67 |
| P3 | 6 | 46.0 |

## Milestones by site

| Site | Ownership | Milestones | Completed |
|---|---|---|---|
| SITE-A | 1P | 5 | 4 |
| SITE-B | 1P | 4 | 3 |
| SITE-C | 3P | 3 | 1 |

## Watch items

- STALE milestone #9 (Partner SLA reporting live, owner partner-mgr): last updated 2026-10-20, 13 days before 2026-11-02.
- STALE milestone #10 (Runbook library v1 published, owner docs-owner): last updated 2026-10-22, 11 days before 2026-11-02.

## How to reproduce every number

Every figure above comes from sql/queries.sql executed against the seeded SQLite database
with as_of = 2026-11-02. See VERIFICATION.md for the query-by-query cross-check.
