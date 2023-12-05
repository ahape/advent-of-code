_id = 0
class Item:
  def __init__(self, val):
    global _id
    self.id = _id
    _id += 1
    self.val = val
    self.occ = []
    self.adjacent_to = set()
  def __str__(self):
    return ("(" + str(self.id) + ") " + 
        self.val + ": " +
        " ".join(self.occ) + " --> " +
        " ".join(map(str, self.adjacent_to)))
  def __repr__(self):
    return self.__str__()

def read_data(file):
  with open(file) as f:
    text = f.read().strip()
    return text.split("\n")

def get_numbers_and_symbols(data):
  numbers = []
  symbols = []
  n = None
  for y, row in enumerate(data):
    for x, cell in enumerate(row):
      if cell.isdigit():
        if n is None:
          n = Item(cell)
        else:
          n.val += cell
        n.occ.append(f"{x},{y}")
      elif cell != ".":
        item = Item(cell)
        item.occ.append(f"{x},{y}")
        symbols.append(item)
      elif n:
        numbers.append(n)
        n = None
  return (numbers, symbols)

def scan_symbol(s, numbers):
  [x,y] = s.occ[0].split(",")
  x = int(x); y = int(y)
  for yi in range(y-1, y+1):
    for xi in range(x-1, x+1):
      print("Check", xi, yi)
      for n in numbers:
        if f"{xi},{yi}" in n.occ:
          print("Hit", n.id)
          n.adjacent_to.add(s.id)

def solve(data):
  numbers, symbols = get_numbers_and_symbols(data)
  for s in symbols:
    scan_symbol(s, numbers)
  for n in numbers:
    print(n)
  for s in symbols:
    print(s)

  return sum([int(n.val) for n in numbers if len(n.adjacent_to)])

def main():
  data = read_data("example-1.txt")
  answer = solve(data)
  print("The Answer:", answer)

if __name__ == "__main__":
  main()
