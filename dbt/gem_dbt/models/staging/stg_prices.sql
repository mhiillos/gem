with source as (

  select * from {{ source('gem','fact_item') }}

),

renamed as (

  select
    id as fact_id,
    item_id,
    high_price,
    low_price,
    high_price_volume,
    low_price_volume,
    window_timestamp

  from source

)

select * from renamed
