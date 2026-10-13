-- 50 highest value items by volume-weighted mean price on the newest complete UTC day
select
  d.price_date,
  d.item_id,
  i.name,
  d.mean_price,
  d.high_price,
  d.low_price,
  d.total_volume as day_volume
from dev_marts.fct_prices_daily as d
join dev_marts.dim_items as i
  on i.item_id = d.item_id
where d.price_date = (select max(price_date) from dev_marts.fct_prices_daily)
order by d.mean_price desc
limit 50;
