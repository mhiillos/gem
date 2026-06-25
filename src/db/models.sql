-- Dimension table: Single item
CREATE TABLE IF NOT EXISTS dim_item (
  item_id INT PRIMARY KEY,
  name TEXT NOT NULL,
  high_alch INT NOT NULL,
  buy_limit INT NOT NULL
);

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'item_type') THEN
    CREATE TYPE item_type AS ENUM ('high', 'low');
  END IF;
END
$$;

-- Fact table: information of an item's price at a specific point in time
CREATE TABLE IF NOT EXISTS fact_item (
  id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  item_id INT NOT NULL,
  price INT NOT NULL,
  timestamp TIMESTAMPTZ NOT NULL,
  type item_type NOT NULL,

  FOREIGN KEY (item_id) REFERENCES dim_item(item_id) ON DELETE CASCADE,
  UNIQUE(item_id, timestamp, type)
);
