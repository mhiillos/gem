-- Finds the most profitable flips from the latest prices.
-- Used for finding quick flips for low buy limit items.
select
  name,
  low_price,
  low_price_volume,
  high_price,
  high_price_volume,
  buy_limit,
  total_volume_24h,
  flip_margin,
  flip_profit_per_limit,
  flip_roi_pct
from dev_marts.mart_items_latest
where buy_limit <= 100 -- Flips for low buy limit items, for quick flips.
and flip_roi_pct > 1 -- Require at least 1% return
and high_price_at >= (now() - interval '2 hour') -- Check against latest prices only
and low_price_volume > 5
and high_price_volume > 5
order by flip_profit_per_limit desc nulls last
limit 50;
