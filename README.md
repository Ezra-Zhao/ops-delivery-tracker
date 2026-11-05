# ops-delivery-tracker

> **SYNTHETIC / SIMULATED DATA - read this first.**
> Every site, milestone, risk, decision, ticket, document, and person-role
> name in this repository is invented for demonstration. Nothing here
> describes a real project, a real employer, a real partner, or real
> operations. No real employer name appears anywhere in this repository.

## What this is

A working, local demonstration of a delivery-tracking and operations
handover system for an infrastructure portfolio that mixes first-party
(1P) and third-party (3P) sites: one portfolio data model (SQLite),
a handover sign-off state machine, a controlled-document register, and
an executive weekly report whose every number is produced by a named
SQL query that anyone can re-run.

It exists to demonstrate the implementation-and-operations side of a
Senior TPM scope: owning a delivery-tracking layer, defining acceptance
and handover requirements, governing controlled information, and taking
an operational tool from discovery to rollout - as a running system with
tests, not only as documents.

## Method sources (honest note)

The working discipline in this system is transferred from the author's
adjacent real experience categories: data-center operations acceptance
and handover (the receiving side of delivered capacity), factory build
and acceptance discipline from server product engineering, and a
risk / dependency / decision governance habit. The gate rules referenced
in the handover workflow come from the author's companion methodology
sample commissioning-gate-kit (referenced by rule name and concept in
docs/05-gate-rules-reference.md; no content is copied from it). This demo
system itself has not run a real portfolio; see "Honest boundaries".

## Run it (all commands reproducible from a clean checkout)

```bash
cd ~/workspace/ops-delivery-tracker

# 1. Build the seeded demo database (synthetic data)
python3 scripts/build_db.py

# 2. Run the handover demo, including one rejected exception
python3 scripts/demo_handover.py

# 3. Generate the one-page executive weekly report
python3 scripts/generate_report.py
#    writes reports/exec-weekly-2026-11-02.md and prints it

# 4. Run the full test suite (23 tests)
python3 -m pytest -q
```

Requirements: Python 3.12 (standard library only at runtime). pytest is
the single dev dependency; if missing: pip install --user pytest.

Reference date for all reporting and staleness: as_of = 2026-11-02
(the seeded "today"), so every run produces identical numbers.

## What is inside

| Area | Where | What it does |
|---|---|---|
| Portfolio data model | odt/schema.sql, odt/db.py | Six core entities - site (with 1P/3P ownership flag), milestone, risk, decision, handover_evidence, ticket - plus handover, post-handover action, and controlled-document tables |
| Stale detection | odt/portfolio.py | A not-completed milestone with no update in over 7 days (configurable) is flagged stale and named in the weekly report |
| Handover workflow | odt/handover.py | State machine: draft, evidence_submitted, under_review, exception_requested, signed_off. Evidence pack enforced; top-severity blockers block sign-off; exceptions need an expiry and a recorded decider on both outcomes; post-handover actions tracked after sign-off |
| Document governance | odt/governance.py | Controlled-document register: version, owner, approval status, supersedes chain, obsolescence flag with mandatory reason; obsolete documents cannot re-enter review or approval |
| Reporting queries | sql/queries.sql | Named, canonical SQL: SLA attainment, MTTR (overall and by priority), milestone achievement, counts, risk and ticket breakdowns |
| Executive report | odt/reporting.py, scripts/generate_report.py, reports/ | One-page markdown weekly, conclusion first; every figure is executed from sql/queries.sql |
| Implementation docs | docs/ | Discovery notes, requirements, integration diagram (assumptions labelled), rollout and adoption plan, gate-rule source reference |
| Seed data | odt/seed.py | Deterministic synthetic seed: 3 sites (2 x 1P, 1 x 3P), 12 milestones, 6 risks, 5 decisions, 20 tickets (16 resolved, 4 open), 4 controlled-document records across 3 documents |
| Tests | tests/ | 23 pytest tests covering SLA/MTTR math, stale flagging, the sign-off flow including a rejected exception, and document version/obsolescence logic |

## JD mapping (target role: TPM, Infrastructure Systems and Tooling)

| JD responsibility area | This repository's counterpart |
|---|---|
| Own the 1P + 3P delivery-tracking layer: milestones, timelines, quantity forecasts, risks, decisions, executive reporting | One SQLite portfolio model with site.ownership separating 1P and 3P (FR-1); milestones carry baseline / forecast / due dates; risk and decision registers are first-class entities; the generated weekly report is the executive surface. Quantity forecast is represented at demo scale by per-site milestone counts and the capacity-forecast milestone in the seed - see Honest boundaries |
| Define capacity acceptance and operational handover requirements | Handover state machine with a fixed evidence pack (test report, checklist, ops readiness note), severity blockers, and recorded sign-off (odt/handover.py) |
| Information governance and controlled document lifecycle | Controlled-document register with versioning, ownership, approval states, supersedes chain, and obsolescence retirement (odt/governance.py, FR-8) |
| Lead end-to-end implementation of operational tooling, discovery to launch | docs/01-discovery-notes.md, docs/02-requirements.md, docs/03-integration-diagram.md, docs/04-rollout-adoption-plan.md (testing/UAT, training, adoption metrics, continuous improvement) plus the running code itself |
| SLA / MTTR reporting (preferred) | sql/queries.sql sla_attainment, mttr, mttr_by_priority, executed by odt/reporting.py and cross-checked in VERIFICATION.md |
| Ticketing workflows (preferred) | Ticket entity with priority-based SLA targets consumed by the reporting layer; the tracker deliberately treats an external ticketing system as the system of record (assumption stated in docs/03) |
| Handover governance (preferred) | Exception (waiver) path with mandatory expiry and recorded decider for both approval and rejection; post-handover action tracking after sign-off |

## Honest boundaries - what this proves and what it does not

- This proves the author can design and implement the system: data model,
  workflow rules, governance logic, reporting math, tests, and the
  implementation document package around them.
- This does not prove the author operated this system, or any equivalent
  tracker, for a real portfolio at a real employer. The data is synthetic,
  the volumes are demo-scale, and no production hardening (auth, access
  control, audit logging, concurrency, notifications) is present or
  claimed; the out-of-scope list in docs/02-requirements.md says so.
- Integration with ticketing and reporting products is drawn as labelled
  design assumptions in docs/03-integration-diagram.md, not built.
- Relationship to the author's other samples: dc-delivery-playbook is a
  document-level delivery playbook and commissioning-gate-kit is a gate
  standards framework. This repository is the running-system counterpart;
  it references the gate kit's rules by name and concept only and copies
  no content from either.

## File list

```
README.md / VERIFICATION.md
odt/__init__.py, odt/db.py, odt/schema.sql, odt/seed.py
odt/portfolio.py, odt/handover.py, odt/governance.py, odt/reporting.py
sql/queries.sql
scripts/build_db.py, scripts/demo_handover.py, scripts/generate_report.py
tests/conftest.py, tests/test_model.py, tests/test_stale.py,
tests/test_handover.py, tests/test_governance.py, tests/test_reporting.py
docs/01-discovery-notes.md, docs/02-requirements.md,
docs/03-integration-diagram.md, docs/04-rollout-adoption-plan.md,
docs/05-gate-rules-reference.md
reports/exec-weekly-2026-11-02.md   (generated)
data/demo.db                        (generated by scripts/build_db.py)
```
