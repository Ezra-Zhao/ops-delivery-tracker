# Rollout and Adoption Plan

> Plan for rolling out a delivery-tracking and handover system of the kind
> demonstrated in this repository. Written as a plan; the only parts already
> executed are the local build and tests described in VERIFICATION.md.

## Phase 0 - Pilot (weeks 1-2)

- Scope: one first-party site plus the tracker owner. Seed the portfolio
  model with the pilot site's live milestones, risks, and decisions.
- Exit criteria: pilot site runs one full handover through the state
  machine, including at least one evidence pack review.
- Testing: workflow walkthrough with the actual sign-off roles; verify the
  stale rule against two weeks of real update behaviour and tune the
  threshold once, on evidence, before wider rollout.

## Phase 1 - Controlled rollout (weeks 3-6)

- Add remaining first-party sites, then third-party (3P) partner sites with
  read/write scoped to their own milestones and evidence.
- UAT: operations leads execute scripted UAT cases mirroring the automated
  tests (happy-path sign-off, missing-evidence block, exception approved,
  exception rejected, obsolete document cannot be approved). UAT sign-off is
  recorded in the decision register - the system governs its own rollout.
- Data migration: historical milestones imported as completed records with
  their original dates; no back-filling of update timestamps, so the stale
  rule starts honest on day one.

## Phase 2 - Reporting cutover (weeks 5-8, overlapping)

- The generated weekly report runs in parallel with the old manual report
  for two cycles; every differing number is reconciled to a query before
  cutover. The manual report is then retired and marked obsolete in the
  document register (the register's first real obsolescence act).
- Executive review adopts the conclusion-first format; feedback is logged
  as requirements, not hallway edits.

## Training

- Role-based, 45 minutes each: site operations leads (milestone hygiene and
  the stale rule), reviewers and sign-off owners (evidence pack and
  exception handling), document owners (versioning and obsolescence),
  executives (how to read the report and re-run a number).
- One-page quick reference per role, itself registered as a controlled
  document so training material cannot silently drift from the workflow.

## Adoption metrics (reviewed weekly during rollout, monthly after)

| Metric | Target | Source |
|---|---|---|
| Milestones updated within 7 days | 90% or more not stale | stale query (odt/portfolio.py) |
| Handovers signed off with a complete evidence pack | 100% (enforced by the state machine) | handover records |
| Exceptions carrying an expiry and a named decider | 100% (enforced) | handover records |
| Weekly report produced from queries, not hand-edited | Every cycle | report generation log |
| Controlled documents with a named owner and current version | 100% of registered docs | document register |
| Active weekly users among named owners | 80% or more by week 6 | usage review in rollout stand-up |

## Continuous improvement

- Monthly: review stale-rule threshold, SLA targets by priority, and the
  evidence pack contents against the last month's exceptions - recurring
  exceptions are a signal the rule, not the teams, needs to change.
- Quarterly: sample closed handovers and re-perform the sign-off checks;
  sample report figures and re-run the queries. Findings go into the risk
  register with owners and decision dates, closing the governance loop.
- The requirement list (02-requirements.md) is a controlled document in
  spirit: changes are versioned, approved, and supersede - never silently
  edited.
