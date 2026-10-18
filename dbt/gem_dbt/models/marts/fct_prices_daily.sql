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
    sum(mean_price * total_volume) / nullif(sum(total_volume), 0) as mean_price,
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
        then lag(mean_price) over w
        else null
    end as prev_mean_price,

    case
      when (lag(price_date) over w = price_date - 1)
        then lag(total_volume) over w
        else null
    end as prev_total_volume

  from daily

  window w as (partition by item_id order by price_date)

),

weekly as (

  select
    c.item_id,
    c.price_date,
    w.high_price as high_price_1w,
    w.low_price as low_price_1w,
    w.mean_price as mean_price_1w,
    w.total_volume as total_volume_1w

  from compared as c
  left join daily as w
    on w.item_id = c.item_id
    and w.price_date = c.price_date - 7

),

diffs as (

  select
    c.item_id,
    c.price_date,
    c.high_price,
    c.high_price_volume,
    c.low_price,
    c.low_price_volume,
    c.mean_price,
    c.total_volume,
    c.hours_traded,

    c.prev_high_price as high_price_prev_day,
    c.prev_low_price as low_price_prev_day,
    c.prev_mean_price as mean_price_prev_day,
    c.prev_total_volume as total_volume_prev_day,
    c.high_price - c.prev_high_price as high_price_change_dod,
    c.low_price - c.prev_low_price as low_price_change_dod,
    c.mean_price - c.prev_mean_price as mean_price_change_dod,
    c.total_volume - c.prev_total_volume as total_volume_change_dod,
    (c.high_price - c.prev_high_price) / c.prev_high_price * 100 as high_price_change_pct_dod,
    (c.low_price - c.prev_low_price) / c.prev_low_price * 100 as low_price_change_pct_dod,
    (c.mean_price - c.prev_mean_price) / c.prev_mean_price * 100 as mean_price_change_pct_dod,
    (c.total_volume - c.prev_total_volume) / nullif(c.prev_total_volume, 0) * 100 as total_volume_change_pct_dod,

    w.high_price_1w as high_price_prev_week,
    w.low_price_1w as low_price_prev_week,
    w.mean_price_1w as mean_price_prev_week,
    w.total_volume_1w as total_volume_prev_week,
    c.high_price - w.high_price_1w as high_price_change_wow,
    c.low_price - w.low_price_1w as low_price_change_wow,
    c.mean_price - w.mean_price_1w as mean_price_change_wow,
    c.total_volume - w.total_volume_1w as total_volume_change_wow,
    (c.high_price - w.high_price_1w) / w.high_price_1w * 100 as high_price_change_pct_wow,
    (c.low_price - w.low_price_1w) / w.low_price_1w * 100 as low_price_change_pct_wow,
    (c.mean_price - w.mean_price_1w) / w.mean_price_1w * 100 as mean_price_change_pct_wow,
    (c.total_volume - w.total_volume_1w) / nullif(w.total_volume_1w, 0) * 100 as total_volume_change_pct_wow

  from compared as c
  left join weekly as w
    on c.item_id = w.item_id
    and c.price_date = w.price_date

),

final as (

  select
    {{ dbt_utils.generate_surrogate_key(['item_id', 'price_date']) }} as price_day_id,
    *

  from diffs

)

select * from final
