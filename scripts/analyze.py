import argparse
from gem.analysis.queries import run_query
from gem.analysis.format import print_table

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("query", type=str)

  args = parser.parse_args()
  rows, headers = run_query(args.query)
  print_table(rows, headers)

if __name__ == "__main__":
  main()

