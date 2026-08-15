from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

def plot(item_name, timestamps, high_prices, low_prices):
  fig, ax = plt.subplots(figsize=(12, 6), layout="constrained")

  ax.plot(
    timestamps,
    high_prices,
    "o-",
    markersize=5,
    linewidth=1.5,
    label="High"
  )

  ax.plot(
    timestamps,
    low_prices,
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
  ax.set_ylim(
    np.nanmin(low_prices) * 0.99,
    np.nanmax(high_prices) * 1.01)

  plt.show()

