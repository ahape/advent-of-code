FILE_NAME = "example_sml.txt"
WALL, BLIZZARD_TYPE, EMPTY = "#", "<v>^", "."
BLIZZ_N, BLIZZ_S, BLIZZ_E, BLIZZ_W = BLIZZARD_TYPE
WALLS, BLIZZARDS = set(), []
ENTRY, EXIT = None, None
DIMS = { "H": 0, "W": 0 }

def draw_frame():
  canvas = []
  for y in range(DIMS["H"]):
    canvas.append(["."] * DIMS["W"])
  for x, y in WALLS:
    canvas[y][x] = WALL
  for c, x, y in BLIZZARDS:
    canvas[y][x] = c
  print("\n".join(map("".join, canvas)))

def load_data():
  global ENTRY, EXIT
  with open(FILE_NAME, "r", encoding="utf-8") as file_in:
    lines = file_in.readlines()
    DIMS["H"] = len(lines)
    for y, line in enumerate(lines):
      if DIMS["W"] == 0:
        DIMS["W"] = len(line)-1
      for x, c in enumerate(line):
        if c == EMPTY:
          if ENTRY is None:
            ENTRY = (x, y)
          else:
            EXIT = (x, y)
        elif c == WALL:
          WALLS.add((x, y))
        elif c in BLIZZARD_TYPE:
          BLIZZARDS.append((c, x, y))

def main():
  load_data()
  draw_frame()

if __name__ == "__main__":
  main()
