with source as (

  select * from {{ source('gem','prices_1h') }}

),

renamed as (

  select

    {{ dbt_utils.generate_surrogate_key(['item_id', "window_timestamp at time zone 'UTC'"]) }} as price_id,

    item_id,
    avg_high_price as high_price,
    coalesce(high_price_volume, 0) as high_price_volume,
    avg_low_price as low_price,
    coalesce(low_price_volume, 0) as low_price_volume,
    window_timestamp,
    _loaded_at,
    _source_file

  from source

)

select * from renamed
