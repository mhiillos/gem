from gem.db.loader import load_prices, load_items
from data import ITEMS, ITEMS2, PRICES, PRICES3, PRICES4

def test_load(test_db):
  load_prices(PRICES)

  with test_db.cursor() as cur:
    cur.execute("""
      SELECT item_id, avg_high_price, avg_low_price, high_price_volume, low_price_volume
      FROM raw.prices_1h
      ORDER BY item_id
    """)

    rows = cur.fetchall()

  assert rows == [
      (1, 10000, 5000, 50, 30),
      (2, 20000, 10000, 20, 15),
      ]

def test_load_duplicates(test_db):
  load_prices(PRICES)
  load_prices(PRICES)

  with test_db.cursor() as cur:
    cur.execute("""
      SELECT COUNT(*)
      FROM raw.prices_1h
    """)
    count = cur.fetchone()[0]

  assert count == 2

def test_load_multiple_prices_for_item(test_db):
  load_prices(PRICES)
  load_prices(PRICES3)

  with test_db.cursor() as cur:
    cur.execute("""
      SELECT avg_high_price
      FROM raw.prices_1h
      WHERE item_id = 1
      ORDER BY window_timestamp
    """)
    prices = [row[0] for row in cur.fetchall()]
    assert prices == [10000, 11000]

def test_load_unknown_item_id(test_db):
  load_prices(PRICES4)
  with test_db.cursor() as cur:
    cur.execute("SELECT COUNT(*) FROM raw.prices_1h")
    assert cur.fetchone()[0] == 1

def test_load_items_replaces_existing(test_db):
  load_items(ITEMS)
  load_items(ITEMS2)

  with test_db.cursor() as cur:
    cur.execute("""
      SELECT id, buy_limit, highalch
      FROM raw.items
      ORDER BY id
    """)
    rows = cur.fetchall()

  assert rows == [
      (1, 32, 11000),
      (2, 8, 1),
      ]

def test_empty_input(test_db):
  load_items([])
  load_prices([])

  with test_db.cursor() as cur:
    cur.execute("SELECT COUNT(*) FROM raw.prices_1h")
    assert cur.fetchone()[0] == 0
    cur.execute("SELECT COUNT(*) FROM raw.items")
    assert cur.fetchone()[0] == 0
