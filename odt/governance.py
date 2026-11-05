"""Controlled-document governance: registration, versioning, approval, obsolescence."""
class GovernanceError(Exception):
    pass
def register_document(conn, doc_code, title, owner, created_at, supersedes_id=None):
    row = conn.execute("SELECT MAX(version) AS v FROM controlled_document WHERE doc_code=?", (doc_code,)).fetchone()
    version = (row["v"] or 0) + 1
    if version > 1 and supersedes_id is None:
        raise GovernanceError("a new version must name the version it supersedes")
    cur = conn.execute(
      "INSERT INTO controlled_document(doc_code,title,version,owner,approval_status,is_obsolete,supersedes_id,created_at) VALUES (?,?,?,?,'draft',0,?,?)",
      (doc_code, title, version, owner, supersedes_id, created_at))
    conn.commit(); return cur.lastrowid, version
def submit_for_review(conn, doc_id):
    r = conn.execute("SELECT * FROM controlled_document WHERE id=?", (doc_id,)).fetchone()
    if r is None: raise GovernanceError("document not found")
    if r["is_obsolete"]: raise GovernanceError("obsolete documents cannot be reviewed")
    if r["approval_status"] != "draft": raise GovernanceError("only draft can move to in_review")
    conn.execute("UPDATE controlled_document SET approval_status='in_review' WHERE id=?", (doc_id,)); conn.commit()
def approve_document(conn, doc_id, by):
    r = conn.execute("SELECT * FROM controlled_document WHERE id=?", (doc_id,)).fetchone()
    if r is None: raise GovernanceError("document not found")
    if r["is_obsolete"]: raise GovernanceError("obsolete documents cannot be approved")
    if r["approval_status"] != "in_review": raise GovernanceError("only in_review can be approved")
    conn.execute("UPDATE controlled_document SET approval_status='approved', approved_by=? WHERE id=?", (by, doc_id)); conn.commit()
def mark_obsolete(conn, doc_id, reason):
    r = conn.execute("SELECT * FROM controlled_document WHERE id=?", (doc_id,)).fetchone()
    if r is None: raise GovernanceError("document not found")
    if r["approval_status"] != "approved": raise GovernanceError("only approved documents are retired via obsolescence")
    if not reason: raise GovernanceError("obsolescence requires a reason")
    conn.execute("UPDATE controlled_document SET is_obsolete=1, obsolete_reason=? WHERE id=?", (reason, doc_id)); conn.commit()
def current_version(conn, doc_code):
    r = conn.execute("SELECT * FROM controlled_document WHERE doc_code=? AND is_obsolete=0 ORDER BY version DESC LIMIT 1", (doc_code,)).fetchone()
    return dict(r) if r else None
