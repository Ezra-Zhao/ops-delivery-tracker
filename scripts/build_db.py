"""Build the seeded demo database: python3 scripts/build_db.py [db_path]"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from odt.db import connect, init_db
from odt.seed import seed_db
if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "data" / "demo.db")
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = init_db(connect(path))
    seed_db(conn)
    n = conn.execute("SELECT COUNT(*) FROM ticket").fetchone()[0]
    print(f"seeded {path}: {n} tickets")
