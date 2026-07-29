-- Returns top items that have the largest percentage difference between high and low price [(high-low)/low]
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
)

SELECT
  d.name,
  l.low_price,
  h.high_price,
  (h.high_price - l.low_price) / l.low_price * 100 AS diff_pct
FROM dim_item d
JOIN latest_high h
  ON d.item_id = h.item_id
JOIN latest_low l
  ON d.item_id = l.item_id
ORDER BY spread_pct DESC
LIMIT 50;
