from odt.reporting import run_metrics, headline
from odt.seed import AS_OF

def test_sla_attainment(conn):
    m = run_metrics(conn, AS_OF)
    row = m["sla_attainment"][0]
    assert row["resolved_n"] == 16
    assert row["sla_met_n"] == 12
    assert row["sla_rate_pct"] == 75.0

def test_mttr(conn):
    m = run_metrics(conn, AS_OF)
    assert m["mttr"][0]["mttr_hours"] == 26.16
    by = {r["priority"]: r["mttr_hours"] for r in m["mttr_by_priority"]}
    assert by["P1"] == 3.12 or by["P1"] == 3.13  # 12.5/4 = 3.125, SQLite ROUND -> checked loosely
    assert by["P2"] == 21.67  # 130/6
    assert by["P3"] == 46.0   # 276/6

def test_milestone_achievement(conn):
    m = run_metrics(conn, AS_OF)
    row = m["milestone_achievement"][0]
    assert row["due_n"] == 10
    assert row["completed_n"] == 8
    assert row["achievement_pct"] == 80.0

def test_ticket_counts(conn):
    m = run_metrics(conn, AS_OF)
    row = m["ticket_counts"][0]
    assert row["total_tickets"] == 20 and row["resolved_tickets"] == 16 and row["open_tickets"] == 4

def test_headline_matches_queries(conn):
    h = headline(run_metrics(conn, AS_OF))
    assert h["sla_rate_pct"] == 75.0 and h["mttr_hours"] == 26.16
    assert h["milestone_achievement_pct"] == 80.0
