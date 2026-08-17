from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

def plot(item_name, timestamps, high_prices, low_prices):
  fig, ax = plt.subplots(figsize=(12, 4), layout="constrained")

  # Remove missing observations so the remaining points are connected
  high_mask = ~np.isnan(high_prices)
  low_mask = ~np.isnan(low_prices)

  ax.plot(
    timestamps[high_mask],
    high_prices[high_mask],
    "o-",
    markersize=5,
    linewidth=1.5,
    label="High"
  )

  ax.plot(
    timestamps[low_mask],
    low_prices[low_mask],
    "o-",
    markersize=5,
    linewidth=1.5,
    label="Low"
  )

  ax.set_title(f"{item_name}: Last 7 days", fontsize=16)
  ax.set_xlabel("Time")
  ax.set_ylabel("Price")

  ax.legend()

  locator = mdates.DayLocator(interval=1)
  formatter = mdates.DateFormatter("%d %b")

  ax.xaxis.set_major_locator(locator)
  ax.xaxis.set_major_formatter(formatter)

  t2 = datetime.now()
  t1 = t2 - timedelta(days=7)
  ax.set_xlim(t1, t2)

  lowest = np.nanmin([low_prices, high_prices])
  highest = np.nanmax([low_prices, high_prices])
  ax.set_ylim(
    np.nanmin(lowest) * 0.99,
    np.nanmax(highest) * 1.01)

  plt.show()

