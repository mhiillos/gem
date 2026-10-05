from datetime import datetime, timedelta, UTC
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

def plot(item_name, timestamps, high_prices, low_prices, volumes):
  _, (ax1, ax2) = plt.subplots(
    2,
    1,
    figsize=(12, 5),
    sharex=True,
    gridspec_kw={"height_ratios": [3, 1]},
    layout="constrained"
   )

  # Remove missing observations -> remaining points are connected
  high_mask = ~np.isnan(high_prices)
  low_mask = ~np.isnan(low_prices)

  # For aligning around midpoint of the hour
  mid = timestamps + timedelta(minutes=30)

  # TODO: Clean up plots
  ax1.plot(
    mid[high_mask],
    high_prices[high_mask],
    "o-",
    markersize=5,
    linewidth=1.5,
    label="High"
  )

  ax1.plot(
    mid[low_mask],
    low_prices[low_mask],
    "o-",
    markersize=5,
    linewidth=1.5,
    label="Low"
  )

  ax1.set_title(f"{item_name}: Last 7 days", fontsize=16)
  ax1.set_xlabel("Time")
  ax1.set_ylabel("Price")

  ax1.legend()

  locator = mdates.DayLocator(interval=1)
  formatter = mdates.DateFormatter("%d %b")

  ax1.xaxis.set_major_locator(locator)
  ax1.xaxis.set_major_formatter(formatter)

  t2 = datetime.now(UTC)
  t1 = t2 - timedelta(days=7)
  ax1.set_xlim(t1, t2)

  lowest = np.nanmin([low_prices, high_prices])
  highest = np.nanmax([low_prices, high_prices])
  ax1.set_ylim(np.nanmin(lowest) * 0.99, np.nanmax(highest) * 1.01)

  # Volumes plot
  # Different color for increased/decreased volumes
  colors = ["tab:blue"]
  for i in range(1, len(volumes)):
    if volumes[i - 1] > volumes[i]:
      colors.append("tab:orange")
    else:
      colors.append("tab:blue")

  ax2.bar(mid, volumes, color=colors, width=(.8/24), align="edge", label="Volume")
  ax2.set_xlabel("Time")
  ax2.set_ylabel("Volume")
  ax2.legend()

  plt.show()
