with source as (

  select * from {{ ref('fct_prices') }}

),

items as (

  select * from {{ ref('dim_items') }}

),

ranked_high as (

  select
    *,
    row_number() over(
      partition by item_id
      order by
        window_timestamp desc
    ) as rn

  from source
  where high_price is not null

),

ranked_low as (

  select
    *,
    row_number() over(
      partition by item_id
      order by
        window_timestamp desc
    ) as rn

  from source
  where low_price is not null

),

latest_high as (

  select
    item_id,
    high_price,
    window_timestamp as high_price_at

  from ranked_high
  where rn = 1

),

latest_low as (

  select
    item_id,
    low_price,
    window_timestamp as low_price_at

  from ranked_low
  where rn = 1

),

ranked_mean as (

  select
    *,
    row_number() over(
      partition by item_id
      order by
        window_timestamp desc
    ) as rn

  from source
  where mean_price is not null

),

latest_mean as (

  select
    item_id,
    mean_price,
    window_timestamp as mean_price_at

  from ranked_mean
  where rn = 1

),

final as (

  select
    items.item_id,
    name,
    icon_url,
    high_alch,
    buy_limit,
    high_price,
    high_price_at,
    low_price,
    low_price_at,
    case
      when high_price_at = low_price_at then (high_price - low_price)
    end as spread,
    mean_price,
    mean_price_at

  from items
  left join latest_high on latest_high.item_id = items.item_id
  left join latest_low on latest_low.item_id = items.item_id
  left join latest_mean on latest_mean.item_id = items.item_id

)

select * from final
