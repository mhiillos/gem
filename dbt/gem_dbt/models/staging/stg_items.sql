with source as (

  select * from {{ source('gem','dim_item') }}

),

renamed as (

  select
    item_id,
    name,
    high_alch as ha_value,
    buy_limit

  from source

)

select * from renamed
