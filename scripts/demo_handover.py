"""Scripted handover demo, including one rejected exception.
Usage: python3 scripts/demo_handover.py
Prints each state transition so VERIFICATION.md can quote the run verbatim."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from odt.db import connect, init_db
from odt.seed import seed_db
from odt import handover as H
if __name__ == "__main__":
    conn = seed_db(init_db(connect()))
    hid = H.create_handover(conn, 2, "Ops handover - Hall B expansion bay", "2026-11-02")
    print(f"created handover #{hid} status=draft")
    for t, title in [("test_report", "Acceptance test report"), ("checklist", "Turnover checklist"), ("ops_readiness", "Ops readiness note")]:
        H.submit_evidence(conn, hid, t, title, f"synthetic-ref-{t}", "tpm-demo", "2026-11-02")
        print(f"submitted evidence {t} -> status=evidence_submitted")
    H.start_review(conn, hid); print("start_review -> status=under_review")
    H.request_exception(conn, hid, "One non-critical checklist annex pending partner countersign", "2026-11-16")
    print("request_exception (expiry 2026-11-16) -> status=exception_requested")
    note = H.decide_exception(conn, hid, approve=False, decider="review-board-demo")
    print(f"decide_exception approve=False -> {note}; status back to under_review")
    row = conn.execute("SELECT status, exception_reason, exception_expiry, exception_decider FROM handover WHERE id=?", (hid,)).fetchone()
    print(f"record after rejection: status={row['status']} reason kept={row['exception_reason']!r} expiry={row['exception_expiry']} decider={row['exception_decider']}")
    H.approve_signoff(conn, hid, "ops-lead-b", "2026-11-02"); print("approve_signoff -> status=signed_off")
    aid = H.add_post_handover_action(conn, hid, "Collect partner countersigned annex", "partner-mgr", "2026-11-16")
    print(f"post-handover action #{aid} created status=open")
    H.complete_post_handover_action(conn, aid); print(f"post-handover action #{aid} completed status=done")
    print(f"open post-handover actions remaining: {len(H.open_post_handover_actions(conn, hid))}")
