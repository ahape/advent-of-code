import re

def read_data(file):
  with open(file) as f:
    text = f.read().strip()
    return text.split("\n")

num_rx = re.compile(r"(\d+)")
def collect_nums_symbols(agg, row):
  matches = num_rx.search(row)

def main():
  data = read_data("example-1.txt")
  answer = solve(data)
  print("The Answer:", answer)

if __name__ == "__main__":
  main()
