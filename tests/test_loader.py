import psycopg
from gem.db.loader import load
import pytest
from data import DIMS, FACTS, FACTS3, FACTS4

def test_load(test_db):
  load(DIMS, FACTS)

  with test_db.cursor() as cur:
    cur.execute("""
      SELECT item_id, price, type
      FROM fact_item
    """)

    rows = cur.fetchall()

  assert rows == [
      (1, 10000, "high"),
      (1, 5000, "low"),
      (2, 20000, "high"),
      (2, 10000, "low"),
      ]

def test_load_duplicates(test_db):
  load(DIMS, FACTS)
  load(DIMS, FACTS)

  with test_db.cursor() as cur:
    cur.execute("""
      SELECT COUNT(*)
      FROM fact_item
    """)
    count = cur.fetchone()[0]

  assert count == 4

def test_load_multiple_prices_for_item(test_db):
  load(DIMS, FACTS)


  load([], FACTS3)

  with test_db.cursor() as cur:
    cur.execute("""
      SELECT price
      FROM fact_item
      WHERE item_id = 1
    """)
    prices = [row[0] for row in cur.fetchall()]
    assert prices == [10000, 5000, 11000]

def test_load_invalid_item_id(test_db):

  with pytest.raises(psycopg.errors.ForeignKeyViolation):
    load([], FACTS4)

def test_empty_input(test_db):
  load([], [])

  with test_db.cursor() as cur:
    cur.execute("SELECT COUNT(*) FROM fact_item")
    assert cur.fetchone()[0] == 0

