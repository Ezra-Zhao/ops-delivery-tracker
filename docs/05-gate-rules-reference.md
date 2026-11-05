# Gate Rules - Source Reference

This system's handover rules are conceptually aligned with the gate
standard in the companion methodology sample commissioning-gate-kit
(a separate local repository by the same author).

## How the reference is used

- Referenced by rule name and decision concept only. No text, tables, or
  wording from that kit are reproduced in this repository.
- The mapping below exists so a reviewer can see where each rule in code
  came from and go read the source standard in the original repository.

| Rule concept in commissioning-gate-kit | Where it lands in this system |
|---|---|
| Gate evidence requirement: a gate passes on attached, accepted evidence, not on a meeting | odt/handover.py REQUIRED_EVIDENCE (test report, checklist, ops readiness note) must all be present before review, and sign-off is a recorded state transition |
| Waiver with expiry: an exception is explicit, records risk and approver, and expires | request_exception refuses an empty expiry; the record keeps reason, expiry, and decider for both approved and rejected outcomes |
| Severity blocks the gate: an open top-severity item prevents exit | blockers() in odt/handover.py: an open P1 ticket for the site, or an open risk with probability x impact of 20 or more, blocks sign-off |
| Escalation is a path, not a person: decisions name the decider and the record persists | Exception decisions record exception_decider; sign-off records signed_off_by and signed_off_at |

## What was adapted, not copied

The gate kit governs commissioning phases for a deploying site; this system
governs portfolio delivery tracking and operational handover. The severity
and evidence concepts transfer; the phase structure does not, and is not
used here.
