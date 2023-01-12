ELF, EMPTY = "#", "."
GRID = []
ELVES = []
SUGG_DIRS = ["N", "S", "W", "E"]

class Elf:
  def set_pos(self, x, y):
    self.x = x
    self.y = y
  
  def check_pos_empty(self, x, y):
    return not any(map(lambda e: e.x == x and e.y == y, ELVES))

  def suggest_pos():
    pass

  def __init__(self, x, y):
    self.set_pos(x, y)

  def __str__(self):
    return "#"

def build_grid(file_in):
  for y, line in enumerate(file_in.readlines()):
    line = line.strip()
    arr = list(line)
    GRID.append(arr)
    for x, c in enumerate(arr):
      if c == "#":
        elf = Elf(x, y)
        GRID[y][x] = elf
        ELVES.append(elf)

def print_grid():
  sb = ""
  for row in GRID:
    sb += f"{''.join(map(str, row))}\n"
  print(sb)

def main():
  with open("example_sml.txt", "r", encoding="utf-8") as file_in:
    build_grid(file_in)

  print_grid()

main()
