"""Generate the one-page executive weekly report.
Usage: python3 scripts/generate_report.py [--as-of 2026-11-02] [--db PATH] [--out PATH]
Builds an in-memory seeded DB by default so the run is reproducible from scratch."""
import argparse, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from odt.db import connect, init_db
from odt.seed import seed_db, AS_OF
from odt.reporting import render_exec_report
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--as-of", default=AS_OF)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    conn = seed_db(init_db(connect()))
    text = render_exec_report(conn, a.as_of)
    out = a.out or str(pathlib.Path(__file__).resolve().parent.parent / "reports" / f"exec-weekly-{a.as_of}.md")
    pathlib.Path(out).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(out).write_text(text, encoding="utf-8")
    print(text)
    print(f"[written] {out}")
