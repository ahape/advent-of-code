FILE_NAME = "example_sml.txt"
WALL, BLIZZARD_TYPE, EMPTY = "#", "<v>^", "."
BLIZZ_N, BLIZZ_S, BLIZZ_E, BLIZZ_W = BLIZZARD_TYPE
WALLS, BLIZZARDS = set(), []
ENTRY, EXIT = None, None

def load_data():
  global ENTRY, EXIT
  with open(FILE_NAME, "r", encoding="utf-8") as file_in:
    for y, line in enumerate(file_in.readlines()):
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

if __name__ == "__main__":
  main()
  print("Blizzards", BLIZZARDS)
  print("Walls", WALLS)
  print("Entry", ENTRY)
  print("Exit", EXIT)
