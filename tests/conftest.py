import os
from pathlib import Path
import pytest
from pytest_postgresql import factories

BASE_PATH = Path(__file__).resolve().parents[1]
SCHEMA = BASE_PATH / "src" / "gem" / "db" / "models.sql"

postgresql_proc = factories.postgresql_proc(
  load=[SCHEMA],
)

postgresql = factories.postgresql("postgresql_proc")

@pytest.fixture
def test_db(postgresql):
  old_db_url = os.environ.get("DB_URL")
  os.environ["DB_URL"] = (
    f"postgresql://"
    f"{postgresql.info.user}@"
    f"{postgresql.info.host}:"
    f"{postgresql.info.port}/"
    f"{postgresql.info.dbname}"
  )

  yield postgresql

  if old_db_url is None:
    os.environ.pop("DB_URL", None)
  else:
    os.environ["DB_URL"] = old_db_url
