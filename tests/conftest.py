import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import pytest
from odt.db import connect, init_db
from odt.seed import seed_db

@pytest.fixture()
def conn():
    c = seed_db(init_db(connect()))
    yield c
    c.close()
