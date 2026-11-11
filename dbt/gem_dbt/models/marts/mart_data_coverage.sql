with bounds as (

  select
    min(window_timestamp) as first_window,
    max(window_timestamp) as last_window
  from {{ ref('fct_prices') }}

),

expected as (

  select generate_series(first_window, last_window, interval '1 hour') as window_timestamp
  from bounds

),

loaded as (

  select distinct window_timestamp
  from {{ ref('fct_prices') }}

),

counts as (

  select
    (select count(*) from expected) as expected_hours,
    (select count(*) from loaded) as loaded_hours

),

final as (

  select
    bounds.first_window,
    bounds.last_window,
    counts.expected_hours,
    counts.loaded_hours,
    counts.expected_hours - counts.loaded_hours as missing_hours,
    round(counts.loaded_hours::numeric / nullif(counts.expected_hours, 0) * 100, 2) as coverage_pct
  from bounds
  cross join counts

)

select * from final
