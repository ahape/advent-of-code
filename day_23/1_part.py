# currently takes 3 seconds per round

import sys, time

ELF, EMPTY = "#", "."
ELVES, GRID = [], []
MIN_X, MIN_Y, MAX_X, MAX_Y = 0, 0, 0, 0
#PAD = 0
PAD = 30
DIR_ORDER = [("N","NE","NW"), ("S","SE","SW"),("W","NW","SW"),("E","NE","SE")]
DIR_MOVE = { "N": -1, "S": 1, "W": -1, "E": 1 }
#FILE_NAME = "example_sml.txt"
#FILE_NAME = "example_lrg.txt"
FILE_NAME = "input.txt"
ids = iter("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" * 200)
DEBUG = sys.argv[-1].lower() == "debug"

class Elf:
  def check_pos_empty(self, x, y, for_movement=False):
    if x < MIN_X or x >= MAX_X:
      if for_movement:
        raise Exception("Reached X boundary")
      return True
    if y < MIN_Y or y >= MAX_Y:
      if for_movement:
        raise Exception("Reached Y boundary")
      return True
    return not any(e.x == x and e.y == y for e in ELVES)

  def can_stay(self):
    return \
        self.check_pos_empty(self.x - 1, self.y - 1) and \
        self.check_pos_empty(self.x + 1, self.y - 1) and \
        self.check_pos_empty(self.x - 1, self.y + 1) and \
        self.check_pos_empty(self.x + 1, self.y + 1) and \
        self.check_pos_empty(self.x - 1, self.y) and \
        self.check_pos_empty(self.x + 1, self.y) and \
        self.check_pos_empty(self.x, self.y - 1) and \
        self.check_pos_empty(self.x, self.y + 1)

  def suggest_pos(self):
    if self.can_stay():
      return None

    for dirs in DIR_ORDER:
      good_sugg = True
      for d in dirs:
        x, y = self.x, self.y
        if "N" in d:
          y -= 1
        elif "S" in d:
          y += 1
        if "E" in d:
          x += 1
        elif "W" in d:
          x -= 1
        if not self.check_pos_empty(x, y, for_movement=True):
          good_sugg = False
          break
      if good_sugg:
        x, y, d = self.x, self.y, dirs[0]
        if d in "WE":
          x += DIR_MOVE[d]
        elif d in "NS":
          y += DIR_MOVE[d]
        return (x, y)
    return None

  def move(self, x, y):
    GRID[self.y][self.x] = EMPTY
    GRID[y][x] = self
    self.x = x
    self.y = y

  def __init__(self, x, y):
    self.id = next(ids)
    self.x = x
    self.y = y

  def __str__(self):
    return self.id if DEBUG else ELF

def get_ground_tiles():
  max_x = max([elf.x for elf in ELVES])+1
  max_y = max([elf.y for elf in ELVES])+1
  min_x = min([elf.x for elf in ELVES])
  min_y = min([elf.y for elf in ELVES])
  empties = 0
  for row in GRID[min_y:max_y]:
    empties += row[min_x:max_x].count(EMPTY)
  return empties

def build_grid(file_in):
  # pylint: disable=W0603
  global MAX_X, MAX_Y, GRID

  def add_y_padding():
    for _ in range(PAD):
      GRID.append([EMPTY] * MAX_X)

  def add_x_padding():
    for i, row in enumerate(GRID):
      GRID[i] = [EMPTY] * PAD + row + [EMPTY] * PAD
    for elf in ELVES:
      elf.x += PAD

  lines = file_in.readlines()

  MAX_X = len(lines[0]) - 1

  add_y_padding()

  for y, line in enumerate(lines):
    y += PAD
    line = line.strip("\n")
    arr = list(line)
    GRID.append(arr)
    for x, c in enumerate(arr):
      if c == ELF:
        elf = GRID[y][x] = Elf(x, y)
        ELVES.append(elf)

  add_y_padding()
  add_x_padding()

  MAX_Y = len(GRID) - 1
  MAX_X = len(GRID[0]) - 1

def print_grid():
  sb = ""
  for i, row in enumerate(GRID):
    row_n = str(i+1).zfill(2)
    printed = ''.join(map(str, row))
    sb += f"{row_n} {printed}\n"
  with open("output.txt", "w", encoding="utf-8") as f:
    f.write(sb)

def rotate_dir_order():
  first = DIR_ORDER[0]
  DIR_ORDER.remove(first)
  DIR_ORDER.append(first)

def get_suggestions():
  suggs = []
  for elf in ELVES:
    suggs.append(elf.suggest_pos())
  for elf, sugg in zip(ELVES, suggs):
    if sugg is not None and suggs.count(sugg) == 1:
      yield elf, sugg

def do_round(round_i):
  suggs = [*get_suggestions()]
  for elf, (x, y) in suggs:
    elf.move(x, y)

  rotate_dir_order()

  print(f"Round {round_i+1}", time.time())
  print_grid()
  return not len(suggs)

def main():
  with open(FILE_NAME, "r", encoding="utf-8") as file_in:
    build_grid(file_in)
  print("Initial state")
  print_grid()
  for n in range(100000000):
    if do_round(n):
      break
  print("Ground tiles", get_ground_tiles())

if __name__ == "__main__":
  # Run the command below to see movement diffs:
  # git diff --no-index --word-diff-regex=. a b
  main()
