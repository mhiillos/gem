-- Biggest week-over-week mean_price movers (point-to-point).
select
  d.name,
  f.mean_price_prev_week,
  f.mean_price,
  f.mean_price_change_wow,
  f.mean_price_change_pct_wow,
  f.total_volume_prev_week,
  f.total_volume
from dev_marts.fct_prices_daily f
left join dev_marts.dim_items d
  on d.item_id = f.item_id
where least(f.total_volume_prev_week, f.total_volume) > 5000
and least(f.mean_price, f.mean_price_prev_week) > 1000
and f.mean_price_change_pct_wow < 500
and f.price_date = (select max(price_date) from dev_marts.fct_prices_daily)
order by abs(f.mean_price_change_pct_wow) desc nulls last
limit 50;
