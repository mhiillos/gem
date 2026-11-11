-- Calculates the volatility of prices, and outputs the items with highest volatility
select
  d.name,
  f.low_price,
  f.high_price,
  f.mean_price,
  f.total_volume,
  f.mean_price_change_pct_wow,
  f.mean_price_volatility_7d
from dev_marts.fct_prices_daily f
left join dev_marts.dim_items d
on d.item_id = f.item_id
where f.price_date = (select max(price_date) from dev_marts.fct_prices_daily)
and f.total_volume > 50
and f.hours_traded > 16
and f.mean_price > 100000
order by f.mean_price_volatility_7d desc nulls last
limit 50;
