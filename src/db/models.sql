-- Dimension table: Single item
CREATE TABLE dim_item (
  item_id INT PRIMARY KEY,
  name TEXT NOT NULL,
  high_alch INT NOT NULL,
  buy_limit INT NOT NULL
);

CREATE TYPE item_type AS ENUM ('high', 'low');

-- Fact table: information of an item's price at a specific point in time
CREATE TABLE fact_item (
  id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  item_id INT NOT NULL,
  price INT NOT NULL,
  timestamp TIMESTAMPTZ NOT NULL,
  type item_type NOT NULL,

  FOREIGN KEY (item_id) REFERENCES dim_item(item_id),
  UNIQUE(item_id, timestamp, type)
);
