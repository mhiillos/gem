-- Checks alch value against current low value for potential profit
WITH latest_low AS (
  SELECT DISTINCT ON (item_id)
    item_id,
    price AS low_price
  FROM fact_item
  WHERE type = 'low'
  ORDER BY item_id, timestamp DESC
)

SELECT
  d.name,
  d.high_alch,
  l.low_price,
  d.buy_limit,
  d.high_alch - l.low_price AS potential_profit,
  (d.high_alch - l.low_price) * 100.0 / l.low_price AS roi
FROM dim_item d
JOIN latest_low l
  ON d.item_id = l.item_id
WHERE d.buy_limit > 8
AND (d.high_alch - l.low_price) * 100.0 / l.low_price < 1000
ORDER BY potential_profit DESC
LIMIT 50;

