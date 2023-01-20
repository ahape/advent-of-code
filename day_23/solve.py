import sys, time

ELF, EMPTY = "#", "."
CURRENT_POSITIONS, ELVES = set(), []
PAD = 5000 # 'Safe' offset used to avoid negative coordinates
DIR_ORDER = [("N","NE","NW"), ("S","SE","SW"),("W","NW","SW"),("E","NE","SE")]
DIR_MOVE_X = { "N": 0, "S": 0, "W": -1, "E": 1, "NE": 1, "NW": -1, "SE": 1, "SW": -1 }
DIR_MOVE_Y = { "N": -1, "S": 1, "W": 0, "E": 0, "NE": -1, "NW": -1, "SE": 1, "SW": 1 }
#FILE_NAME = "example_sml.txt"
#FILE_NAME = "example_lrg.txt"
FILE_NAME = "input.txt"
PART_1 = sys.argv[-1].lower() == "1"

class Elf:
  def check_pos_empty(self, x, y):
    return (x, y) not in CURRENT_POSITIONS

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
    x, y = self.x, self.y
    for a, b, c in DIR_ORDER:
      if self.check_pos_empty(x + DIR_MOVE_X[a], y + DIR_MOVE_Y[a]) and \
         self.check_pos_empty(x + DIR_MOVE_X[b], y + DIR_MOVE_Y[b]) and \
         self.check_pos_empty(x + DIR_MOVE_X[c], y + DIR_MOVE_Y[c]):
        return (x + DIR_MOVE_X[a], y + DIR_MOVE_Y[a])
    return None

  def move(self, x, y):
    CURRENT_POSITIONS.remove((self.x, self.y))
    CURRENT_POSITIONS.add((x, y))
    self.x = x
    self.y = y

  def __init__(self, x, y):
    self.x = x
    self.y = y
    CURRENT_POSITIONS.add((x, y))

def get_ground_tiles():
  min_x, max_x, min_y, max_y = get_ranges()
  return (max_x - min_x) * (max_y - min_y) - len(ELVES)

def build_grid(file_in):
  lines = file_in.readlines()

  for y, line in enumerate(lines):
    y += PAD
    for x, c in enumerate(line.strip("\n")):
      if c == ELF:
        ELVES.append(Elf(x + PAD, y + PAD))

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

def do_round(round_n):
  suggs = [*get_suggestions()]
  for elf, (x, y) in suggs:
    elf.move(x, y)

  rotate_dir_order()

  #print(f"Round {round_n}")
  return len(suggs) == 0

def get_ranges():
  xset, yset = set(), set()
  for (x, y) in CURRENT_POSITIONS:
    xset.add(x)
    yset.add(y)
  return (min(xset), max(xset)+1, min(yset), max(yset)+1)

def print_grid():
  """
  For debugging
  """
  min_x, max_x, min_y, max_y = get_ranges()
  output = ""
  for y in range(min_y, max_y):
    row = ""
    for x in range(min_x, max_x):
      if (x, y) in CURRENT_POSITIONS:
        row += ELF
      else:
        row += EMPTY
    output += row + "\n"
  print(output)

def main():
  with open(FILE_NAME, "r", encoding="utf-8") as file_in:
    build_grid(file_in)
  n = 1
  start_time = time.time()
  while not PART_1 or n <= 10:
    if do_round(n):
      break
    n += 1

  if PART_1:
    print("Ground tiles", get_ground_tiles())
  else:
    print(f"Total rounds {n} in {time.time() - start_time} seconds")

if __name__ == "__main__":
  main()
