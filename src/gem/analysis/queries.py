from pathlib import Path
from gem.db.connection import get_connection

SQL_DIR = Path(__file__).resolve().parents[3] / "sql"

def run_query(query, params=None):
  path = SQL_DIR / f"{query}.sql"
  if not path.exists():
    raise FileNotFoundError

  sql = (SQL_DIR / f"{query}.sql").read_text()
  with get_connection() as conn:
    with conn.cursor() as cur:
      cur.execute(sql, params)
      return cur.fetchall(), [desc[0] for desc in cur.description]

