from pathlib import Path
from src.db.connection import get_connection

SQL_DIR = Path(__file__).resolve().parents[2] / "sql"

def run_query(query):
  sql = (SQL_DIR / f"{query}.sql").read_text()
  with get_connection() as conn:
    with conn.cursor() as cur:
      cur.execute(sql)
      return cur.fetchall(), [desc[0] for desc in cur.description]

