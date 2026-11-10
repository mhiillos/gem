{% docs item_id %}
OSRS item id.
{% enddocs %}

{% docs window_timestamp %}
Start of the 1-hour price window, UTC.
{% enddocs %}

{% docs price_id %}
Surrogate key of `item_id` and `window_timestamp`.
{% enddocs %}

{% docs high_price %}
Average instant-buy price. NULL when not traded.
{% enddocs %}

{% docs low_price %}
Average instant-sell price. NULL when not traded.
{% enddocs %}

{% docs high_price_volume %}
Items traded at the instant-buy price.
{% enddocs %}

{% docs low_price_volume %}
Items traded at the instant-sell price.
{% enddocs %}

{% docs total_volume %}
Items traded on both sides.
{% enddocs %}

{% docs mean_price %}
Volume-weighted average price of both sides.
{% enddocs %}

{% docs spread %}
`high_price - low_price`. NULL unless both sides traded.
{% enddocs %}

{% docs spread_pct %}
Spread as a % of `low_price`.
{% enddocs %}

{% docs prev_day %}
Value on the previous day. NULL if the item didn't trade that day.
{% enddocs %}

{% docs change_dod %}
Change from the previous day.
{% enddocs %}

{% docs change_pct_dod %}
Change from the previous day, in %.
{% enddocs %}

{% docs prev_week %}
Value 7 days earlier. NULL if the item didn't trade that day.
{% enddocs %}

{% docs change_wow %}
Change from 7 days earlier.
{% enddocs %}

{% docs change_pct_wow %}
Change from 7 days earlier, in %.
{% enddocs %}

{% docs loaded_at %}
When the row was loaded into the raw table.
{% enddocs %}

{% docs source_file %}
Archive file the row was loaded from.
{% enddocs %}
