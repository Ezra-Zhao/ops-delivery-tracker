import pytest
from odt import handover as H

def _ready(conn, site_id=2):
    hid = H.create_handover(conn, site_id, "Demo handover", "2026-11-02")
    for t in H.REQUIRED_EVIDENCE:
        H.submit_evidence(conn, hid, t, f"{t} doc", f"ref-{t}", "tpm-demo", "2026-11-02")
    H.start_review(conn, hid)
    return hid

def test_happy_path_signoff_and_post_actions(conn):
    hid = _ready(conn)
    H.approve_signoff(conn, hid, "ops-lead-b", "2026-11-02")
    row = conn.execute("SELECT status, signed_off_by FROM handover WHERE id=?", (hid,)).fetchone()
    assert row["status"] == "signed_off" and row["signed_off_by"] == "ops-lead-b"
    aid = H.add_post_handover_action(conn, hid, "Follow-up item", "partner-mgr", "2026-11-16")
    assert len(H.open_post_handover_actions(conn, hid)) == 1
    H.complete_post_handover_action(conn, aid)
    assert H.open_post_handover_actions(conn, hid) == []

def test_missing_evidence_blocks_review(conn):
    hid = H.create_handover(conn, 2, "Incomplete handover", "2026-11-02")
    H.submit_evidence(conn, hid, "test_report", "only one", "ref-1", "tpm-demo", "2026-11-02")
    with pytest.raises(H.WorkflowError):
        H.start_review(conn, hid)

def test_exception_rejected(conn):
    hid = _ready(conn)
    H.request_exception(conn, hid, "Annex pending countersign", "2026-11-16")
    note = H.decide_exception(conn, hid, approve=False, decider="review-board-demo")
    assert note == "exception_rejected"
    row = conn.execute("SELECT status, exception_decider FROM handover WHERE id=?", (hid,)).fetchone()
    assert row["status"] == "under_review" and row["exception_decider"] == "review-board-demo"

def test_exception_approved(conn):
    hid = _ready(conn)
    H.request_exception(conn, hid, "Minor annex delay", "2026-11-16")
    note = H.decide_exception(conn, hid, approve=True, decider="review-board-demo")
    assert note == "exception_approved"
    H.approve_signoff(conn, hid, "ops-lead-b", "2026-11-02")

def test_exception_requires_expiry(conn):
    hid = _ready(conn)
    with pytest.raises(H.WorkflowError):
        H.request_exception(conn, hid, "No expiry given", "")

def test_p1_blocker_blocks_signoff(conn):
    # Site 1 has no open P1 in seed, so add one and confirm the severity block fires.
    conn.execute("INSERT INTO ticket VALUES (99, 1, 'Open P1 demo', 'P1', 4, 'open', '2026-11-02 08:00', NULL, 'network')")
    conn.commit()
    hid = _ready(conn, site_id=1)
    with pytest.raises(H.WorkflowError):
        H.approve_signoff(conn, hid, "ops-lead-a", "2026-11-02")

def test_post_action_requires_signoff(conn):
    hid = _ready(conn)
    with pytest.raises(H.WorkflowError):
        H.add_post_handover_action(conn, hid, "Too early", "owner", "2026-11-16")
