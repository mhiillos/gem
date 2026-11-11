# Prettifies printing

from decimal import Decimal
from tabulate import tabulate

def format_number(value):
  if not isinstance(value, (int, float, Decimal)):
    return value
  if isinstance(value, bool):
    return value

  if abs(value) >= 1_000_000_000:
    value = f"{value / 1_000_000_000:.3f}B"
  elif abs(value) >= 1_000_000:
    value = f"{value / 1_000_000:.3f}M"
  else:
    if isinstance(value, (Decimal, float)):
      value = f"{value:,.2f}"
    elif isinstance(value, int):
      value = f"{value:,}"
  return value

def print_table(rows, headers):
  formatted = [[format_number(value) for value in row] for row in rows]
  print(tabulate(formatted, headers=headers, disable_numparse=True))
