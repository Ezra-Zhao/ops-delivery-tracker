"""Reporting: executes sql/queries.sql verbatim and renders the exec report."""
import pathlib

QUERIES_FILE = pathlib.Path(__file__).resolve().parent.parent / "sql" / "queries.sql"

def load_queries(path=None):
    text = (path or QUERIES_FILE).read_text(encoding="utf-8")
    queries, name, buf = {}, None, []
    for line in text.splitlines():
        if line.strip().startswith("-- name:"):
            if name:
                queries[name] = "\n".join(buf).strip().rstrip(";")
            name = line.strip().split(":", 1)[1].strip()
            buf = []
        elif name is not None:
            if line.strip().startswith("--"):
                continue
            buf.append(line)
    if name:
        queries[name] = "\n".join(buf).strip().rstrip(";")
    return queries

def run_metrics(conn, as_of):
    q = load_queries()
    params = {"as_of": as_of}
    out = {}
    for name, sql in q.items():
        try:
            rows = conn.execute(sql, params).fetchall()
        except Exception:
            rows = conn.execute(sql).fetchall()
        out[name] = [dict(r) for r in rows]
    return out

def headline(metrics):
    sla = metrics["sla_attainment"][0]
    mttr = metrics["mttr"][0]
    ms = metrics["milestone_achievement"][0]
    counts = metrics["ticket_counts"][0]
    return {
        "sla_rate_pct": sla["sla_rate_pct"], "sla_met_n": sla["sla_met_n"],
        "resolved_n": sla["resolved_n"], "mttr_hours": mttr["mttr_hours"],
        "milestone_achievement_pct": ms["achievement_pct"],
        "milestones_completed": ms["completed_n"], "milestones_due": ms["due_n"],
        "total_tickets": counts["total_tickets"], "open_tickets": counts["open_tickets"],
    }

def render_exec_report(conn, as_of, stale_days=7):
    from odt.portfolio import stale_milestones
    m = run_metrics(conn, as_of)
    h = headline(m)
    stale = stale_milestones(conn, as_of, stale_days)
    risks = m["open_risks_by_severity"]
    risk_line = ", ".join(f"{r['severity']}: {r['n']}" for r in risks) if risks else "none"
    by_pri = m["mttr_by_priority"]
    pri_lines = "\n".join(
        f"| {r['priority']} | {r['resolved_n']} | {r['mttr_hours']} |" for r in by_pri)
    site_lines = "\n".join(
        f"| {r['site_code']} | {r['ownership']} | {r['milestones']} | {r['completed']} |"
        for r in m["milestones_by_site"])
    if h["sla_rate_pct"] >= 85 and h["milestone_achievement_pct"] >= 80:
        verdict = "Portfolio is on track overall; the watch items below are the exceptions, not the trend."
    else:
        verdict = "Portfolio needs attention: at least one headline metric is below its target line (SLA 85%, milestone achievement 80%)."
    lines = []
    lines.append(f"# Executive Weekly Report - Operations Delivery Portfolio (week ending {as_of})")
    lines.append("")
    lines.append("> SYNTHETIC / SIMULATED DATA - generated from the seeded demo database. Not a real portfolio.")
    lines.append("")
    lines.append("## Bottom line first")
    lines.append("")
    lines.append(verdict)
    lines.append(f"- SLA attainment: {h['sla_rate_pct']}% ({h['sla_met_n']} of {h['resolved_n']} resolved tickets met SLA).")
    lines.append(f"- MTTR: {h['mttr_hours']} hours across {h['resolved_n']} resolved tickets.")
    lines.append(f"- Milestone achievement (due to date): {h['milestone_achievement_pct']}% ({h['milestones_completed']} of {h['milestones_due']} due milestones completed).")
    lines.append(f"- Open tickets: {h['open_tickets']} of {h['total_tickets']} total. Stale milestones (no update in over {stale_days} days, not completed): {len(stale)}.")
    lines.append(f"- Open risks by severity: {risk_line}.")
    lines.append("")
    lines.append("## MTTR by priority (hours)")
    lines.append("")
    lines.append("| Priority | Resolved | MTTR hours |")
    lines.append("|---|---|---|")
    lines.append(pri_lines)
    lines.append("")
    lines.append("## Milestones by site")
    lines.append("")
    lines.append("| Site | Ownership | Milestones | Completed |")
    lines.append("|---|---|---|---|")
    lines.append(site_lines)
    lines.append("")
    lines.append("## Watch items")
    lines.append("")
    if stale:
        for s in stale:
            lines.append(f"- STALE milestone #{s['id']} ({s['name']}, owner {s['owner']}): last updated {s['updated_at']}, {s['age_days']} days before {as_of}.")
    else:
        lines.append("- No stale milestones.")
    lines.append("")
    lines.append("## How to reproduce every number")
    lines.append("")
    lines.append("Every figure above comes from sql/queries.sql executed against the seeded SQLite database")
    lines.append(f"with as_of = {as_of}. See VERIFICATION.md for the query-by-query cross-check.")
    lines.append("")
    return "\n".join(lines)
