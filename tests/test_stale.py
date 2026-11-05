from odt.portfolio import stale_milestones, milestone_health
from odt.seed import AS_OF

def test_stale_set(conn):
    stale = stale_milestones(conn, AS_OF, stale_days=7)
    assert {m["id"] for m in stale} == {9, 10}
    assert all(m["flag"] == "stale" for m in stale)

def test_stale_boundary_not_flagged(conn):
    # Milestone 12 updated 2026-10-30, as_of 2026-11-02 -> 3 days, current.
    # Milestone 11 updated 2026-11-01 -> 1 day, current. Completed ones never stale.
    health = {m["id"]: m["flag"] for m in milestone_health(conn, AS_OF, stale_days=7)}
    assert health[11] == "current" and health[12] == "current"
    assert health[1] == "done"

def test_stale_threshold_configurable(conn):
    assert stale_milestones(conn, AS_OF, stale_days=14) == []
    assert {m["id"] for m in stale_milestones(conn, AS_OF, stale_days=10)} == {9, 10}
