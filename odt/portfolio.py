from datetime import date
def _d(s):
    return date.fromisoformat(s)
def stale_milestones(conn, as_of, stale_days=7):
    """Milestones not completed whose updated_at is more than stale_days before as_of.
    Returns list of dicts with age_days and flag='stale'. Boundary: exactly stale_days is NOT stale."""
    as_of_d = _d(as_of)
    out = []
    for r in conn.execute("SELECT * FROM milestone WHERE status != 'completed' ORDER BY id"):
        age = (as_of_d - _d(r["updated_at"])).days
        if age > stale_days:
            d = dict(r); d["age_days"] = age; d["flag"] = "stale"
            out.append(d)
    return out
def milestone_health(conn, as_of, stale_days=7):
    stale_ids = {m["id"] for m in stale_milestones(conn, as_of, stale_days)}
    rows = []
    for r in conn.execute("SELECT * FROM milestone ORDER BY id"):
        d = dict(r)
        d["flag"] = "stale" if d["id"] in stale_ids else ("done" if d["status"]=="completed" else "current")
        rows.append(d)
    return rows
