"""Handover sign-off state machine.

Gate-rule source (concept reference only, no text copied):
commissioning-gate-kit -- rules referenced by name/concept:
  (a) gate evidence requirement: a gate does not pass on a meeting alone;
      named evidence must be attached and accepted.
  (b) waiver / exception must be explicit and must carry an expiry.
  (c) severity block: an open Sev1/Sev2-equivalent blocker (here: an open
      P1 ticket for the site, or an open risk with probability*impact >= 20)
      blocks sign-off.
  (d) escalation is a recorded path: exception decisions record decider.
States: draft -> evidence_submitted -> under_review -> signed_off
        under_review -> exception_requested -> under_review (approved, waiver noted)
                                                 -> under_review (rejected, reason kept)
"""
REQUIRED_EVIDENCE = ("test_report", "checklist", "ops_readiness")
class WorkflowError(Exception):
    pass
def create_handover(conn, site_id, title, created_at):
    cur = conn.execute("INSERT INTO handover(site_id,title,status,created_at) VALUES (?,?,?,?)",
                       (site_id, title, "draft", created_at))
    conn.commit(); return cur.lastrowid
def _get(conn, hid):
    r = conn.execute("SELECT * FROM handover WHERE id=?", (hid,)).fetchone()
    if r is None: raise WorkflowError("handover not found")
    return r
def _set(conn, hid, status, **kw):
    cols = ", ".join([f"{k}=?" for k in kw])
    sql = f"UPDATE handover SET status=?{(', '+cols) if cols else ''} WHERE id=?"
    conn.execute(sql, [status, *kw.values(), hid]); conn.commit()
def submit_evidence(conn, hid, evidence_type, title, reference, by, at):
    h = _get(conn, hid)
    if h["status"] not in ("draft", "evidence_submitted"):
        raise WorkflowError(f"cannot submit evidence from status {h['status']}")
    conn.execute("INSERT INTO handover_evidence(handover_id,evidence_type,title,reference,submitted_by,submitted_at,accepted) VALUES (?,?,?,?,?,?,1)",
                 (hid, evidence_type, title, reference, by, at))
    conn.commit()
    _set(conn, hid, "evidence_submitted")
def missing_evidence(conn, hid):
    have = {r[0] for r in conn.execute("SELECT DISTINCT evidence_type FROM handover_evidence WHERE handover_id=? AND accepted=1", (hid,))}
    return [t for t in REQUIRED_EVIDENCE if t not in have]
def start_review(conn, hid):
    h = _get(conn, hid)
    if h["status"] != "evidence_submitted":
        raise WorkflowError(f"cannot start review from status {h['status']}")
    miss = missing_evidence(conn, hid)
    if miss: raise WorkflowError(f"missing required evidence: {miss}")
    _set(conn, hid, "under_review")
def blockers(conn, hid):
    h = _get(conn, hid); out = []
    n = conn.execute("SELECT COUNT(*) FROM ticket WHERE site_id=? AND priority='P1' AND status='open'", (h["site_id"],)).fetchone()[0]
    if n: out.append(f"{n} open P1 ticket(s) for site")
    for r in conn.execute("SELECT title, probability*impact AS score FROM risk WHERE site_id=? AND status='open'", (h["site_id"],)):
        if r["score"] >= 20: out.append(f"high-exposure open risk: {r['title']} (score {r['score']})")
    return out
def approve_signoff(conn, hid, by, at):
    h = _get(conn, hid)
    if h["status"] != "under_review":
        raise WorkflowError(f"cannot sign off from status {h['status']}")
    b = blockers(conn, hid)
    if b: raise WorkflowError(f"sign-off blocked: {b}")
    _set(conn, hid, "signed_off", signed_off_by=by, signed_off_at=at)
def request_exception(conn, hid, reason, expiry):
    h = _get(conn, hid)
    if h["status"] != "under_review":
        raise WorkflowError(f"cannot request exception from status {h['status']}")
    if not expiry: raise WorkflowError("exception (waiver) must carry an expiry -- gate rule (b)")
    _set(conn, hid, "exception_requested", exception_reason=reason, exception_expiry=expiry)
def decide_exception(conn, hid, approve, decider):
    h = _get(conn, hid)
    if h["status"] != "exception_requested":
        raise WorkflowError(f"cannot decide exception from status {h['status']}")
    # Both outcomes return to under_review; approval is recorded in the
    # exception fields, rejection keeps the reason and clears nothing silently.
    status_note = "exception_approved" if approve else "exception_rejected"
    conn.execute("UPDATE handover SET status='under_review', exception_decider=? WHERE id=?", (decider, hid))
    conn.commit()
    return status_note
def add_post_handover_action(conn, hid, title, owner, due_date):
    h = _get(conn, hid)
    if h["status"] != "signed_off":
        raise WorkflowError("post-handover actions require a signed-off handover")
    cur = conn.execute("INSERT INTO post_handover_action(handover_id,title,owner,due_date,status) VALUES (?,?,?,?,'open')",
                       (hid, title, owner, due_date))
    conn.commit(); return cur.lastrowid
def complete_post_handover_action(conn, action_id):
    conn.execute("UPDATE post_handover_action SET status='done' WHERE id=?", (action_id,)); conn.commit()
def open_post_handover_actions(conn, hid):
    return [dict(r) for r in conn.execute("SELECT * FROM post_handover_action WHERE handover_id=? AND status!='done' ORDER BY id", (hid,))]
