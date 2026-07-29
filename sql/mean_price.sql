-- Calculate the latest mean price for every item [(high + low) / 2], and return all items with a mean price between 50m and 150m (million).
WITH latest_high AS (
  SELECT DISTINCT ON (item_id)
    item_id,
    price AS high_price
  FROM fact_item
  WHERE type = 'high'
  ORDER BY item_id, timestamp DESC
),

latest_low AS (
  SELECT DISTINCT ON (item_id)
    item_id,
    price AS low_price
  FROM fact_item
  WHERE type = 'low'
  ORDER BY item_id, timestamp DESC
),

mean_prices AS (
SELECT
  d.name,
  h.high_price,
  l.low_price,
    (h.high_price + l.low_price) / 2 AS mean_price
FROM dim_item d
JOIN latest_high h
  ON d.item_id = h.item_id
JOIN latest_low l
  ON d.item_id = l.item_id
)

SELECT * from mean_prices
WHERE mean_price BETWEEN 50000000 AND 150000000
ORDER BY mean_price DESC;

