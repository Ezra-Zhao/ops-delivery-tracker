# Workflow Discovery Notes (Design Phase)

> SYNTHETIC / SIMULATED - discovery notes for a methodology demo. No real
> employer, site, partner, or stakeholder is described anywhere in this file.

## What discovery set out to answer

Before building anything, the implementation had to answer four questions:

1. What does the delivery-tracking layer actually track today, and where does
   the truth live - spreadsheet, ticket queue, chat, or someone's memory?
2. Where do handovers fail: missing evidence, unclear acceptance criteria,
   or no named owner after sign-off?
3. Which numbers do executives actually read, and can each number be traced
   back to a query anyone can re-run?
4. What must be governed as controlled information (versions, owners,
   approval state, retirement) versus what is just working chatter?

## Method used (as designed for this demo)

- Stakeholder interviews by role, not by team: site operations lead, partner
  manager for third-party (3P) capacity, tooling owner, document owner,
  executive consumer of the weekly report.
- Artifact walk-through: take one recent (simulated) handover and trace every
  artifact it touched, in order, noting each manual re-entry of the same fact.
- Ticket archaeology: sample closed tickets and check whether SLA and
  resolution time can be computed from the recorded timestamps alone. If a
  field needed for SLA/MTTR is not captured at creation, the workflow - not
  the report - is what gets fixed.
- Shadowing the weekly reporting ritual: who assembles it, from what, and
  how long reconciliation takes when two trackers disagree.

## Findings that shaped the build

1. Two trackers (one for first-party, one for partner sites) made the
   portfolio roll-up a manual merge. Design response: one data model, with
   an ownership flag (1P / 3P) on the site entity instead of two systems.
2. Handovers were declared done in meetings with no evidence pack attached.
   Design response: sign-off is a state machine that cannot reach
   signed_off without three named evidence types accepted first.
3. Milestones went quietly stale - nobody owned noticing. Design response:
   a stale rule (no update in over 7 days, not completed) computed from
   data, surfaced in the weekly report as a named watch item.
4. Documents lived as attachments with no version or retirement state.
   Design response: a controlled-document register with version, owner,
   approval status, and an explicit obsolescence flag with reason.
5. Executive numbers could not be reproduced after the meeting. Design
   response: every report figure is one named SQL query in
   sql/queries.sql; the report is generated, never hand-typed.

## Open questions left for a real deployment (not answered by this demo)

- Identity and access: who may sign off, and how is a 3P partner scoped to
  only its own sites? (This demo models roles as plain owner strings.)
- Retention and audit requirements for handover evidence in a regulated
  environment.
- Whether the ticketing system of record remains external (see the
  integration assumptions in 03-integration-diagram.md).
