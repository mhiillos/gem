with source as (

  select * from {{ ref('fct_prices') }}

),

daily as (

  select
    item_id,
    (window_timestamp at time zone 'UTC')::date as price_date,
    sum(high_price * high_price_volume) / nullif(sum(high_price_volume), 0) as high_price,
    sum(high_price_volume) as high_price_volume,
    sum(low_price * low_price_volume) / nullif(sum(low_price_volume), 0) as low_price,
    sum(low_price_volume) as low_price_volume,
    sum(total_volume) as total_volume,
    count(*) as hours_traded

  from source
  where (window_timestamp at time zone 'UTC')::date
    < (select max(window_timestamp at time zone 'UTC')::date from source)
  group by item_id, price_date

),

compared as (

  select
    *,
    case
      when (lag(price_date) over w = price_date - 1)
        then lag(high_price) over w
        else null
    end as prev_high_price,

    case
      when (lag(price_date) over w = price_date - 1)
        then lag(low_price) over w
        else null
    end as prev_low_price,

    case
      when (lag(price_date) over w = price_date - 1)
        then lag(total_volume) over w
        else null
    end as prev_total_volume

  from daily

  window w as (partition by item_id order by price_date)

),

diffs as (

  select
    *,
    high_price - prev_high_price as high_price_change,
    low_price - prev_low_price as low_price_change,
    total_volume - prev_total_volume as total_volume_change,
    (high_price - prev_high_price) / prev_high_price * 100 as high_price_change_pct,
    (low_price - prev_low_price) / prev_low_price * 100 as low_price_change_pct,
    (total_volume - prev_total_volume) / nullif(prev_total_volume, 0) * 100 as total_volume_change_pct

  from compared

),

final as (

  select
    {{ dbt_utils.generate_surrogate_key(['item_id', 'price_date']) }} as price_day_id,
    *

  from diffs

)

select * from final
