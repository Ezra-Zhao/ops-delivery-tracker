def test_six_core_entities_exist(conn):
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    for t in ("site", "milestone", "risk", "decision", "handover_evidence", "ticket"):
        assert t in tables

def test_site_ownership_mix(conn):
    rows = {r["code"]: r["ownership"] for r in conn.execute("SELECT code, ownership FROM site")}
    assert rows == {"SITE-A": "1P", "SITE-B": "1P", "SITE-C": "3P"}

def test_seed_counts(conn):
    assert conn.execute("SELECT COUNT(*) FROM milestone").fetchone()[0] == 12
    assert conn.execute("SELECT COUNT(*) FROM risk").fetchone()[0] == 6
    assert conn.execute("SELECT COUNT(*) FROM decision").fetchone()[0] == 5
