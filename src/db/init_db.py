from connection import get_connection
from pathlib import Path
import sys

DB_URL = "postgresql://postgres@localhost:5432/gem_db"

def read_schema(path):
  with open(path, "r") as f:
    schema = f.read()
  return schema

def main():
  with get_connection(DB_URL) as conn:
    base_path = Path(__file__).resolve().parents[2]
    models_path = base_path / "src" / "db" / "models.sql"
    schema = read_schema(models_path)

    with conn.cursor() as cur:
      try:
        cur.execute(schema)
      except Exception as e:
        sys.stderr.write(f"[gem] Error initializing database, rolling back: {e}\n")
        conn.rollback()
        raise e

      conn.commit()

if __name__ == "__main__":
  main()

