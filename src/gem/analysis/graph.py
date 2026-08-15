from gem.analysis.queries import run_query
from gem.analysis.plot import plot
import numpy as np

def graph(item_name):
  rows, _ = run_query("item_graph_7d", (item_name,))

  timestamps = np.array([x[0] for x in rows])
  high_prices = np.array([x[1] for x in rows], dtype=float)
  low_prices = np.array([x[2] for x in rows], dtype=float)

  print(high_prices)
  print(low_prices)
  plot(
      item_name,
      timestamps,
      high_prices,
      low_prices,
      )
