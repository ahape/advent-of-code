POS = None
canvas = []
GLYPHS = ">v<^"
DIRS = "ESWN"
DIMS = (0, 0)
#SIDE_SIZE = 4
SIDE_SIZE = 50

next_side = {}

if SIDE_SIZE == 4:
  next_side["1N"] = "2Nn"
  next_side["1E"] = "6Wn"
  next_side["1W"] = "3Sn"
  next_side["2N"] = "1Sn"
  next_side["2S"] = "5Nn"
  next_side["2W"] = "6Nn"
  next_side["3N"] = "1En"
  next_side["3S"] = "5En"
  next_side["4E"] = "6Sn"
  next_side["5S"] = "2Nn"
  next_side["5W"] = "3Nn"
  next_side["6N"] = "4Wn"
  next_side["6S"] = "2Wn"
  next_side["6E"] = "1Wn"
else:
  next_side["1N"] = "6En"
  next_side["1W"] = "4Ey" #mirrored?
  next_side["2N"] = "6Nn"
  next_side["2E"] = "5Wy" #mirrored?
  next_side["2S"] = "3Wn"
  next_side["3E"] = "2Nn"
  next_side["3W"] = "4Sn"
  next_side["5E"] = "2Wy" #mirrored?
  next_side["5S"] = "6Wn"
  next_side["4N"] = "3En"
  next_side["4W"] = "1Ey" #m?
  next_side["6E"] = "5Nn"
  next_side["6S"] = "2Sn"
  next_side["6W"] = "1SN"

class Instruction():
  """
  Represents an instruction.
  When an instruction is executed, the distance is traveled,
  and then the cursor turns to the direction
  """
  def __init__(self):
    self.direction = None
    self.distance = 0

  def __str__(self):
    return f"{self.distance}:{self.direction}"

  def __repr__(self):
    return self.__str__()

def parse_instructions(instructions_raw):
  builder = []
  instruction = Instruction()
  distance = ""
  for e in instructions_raw:
    if e in ("L", "R"):
      instruction.distance += int(distance)
      distance = ""
      instruction.direction = e
      builder.append(instruction)
      instruction = Instruction()
    else:
      distance += e
  instruction.direction = None
  instruction.distance = int(distance)
  builder.append(instruction)
  return builder

def parse_line(raw_line):
  if not raw_line.strip():
    return (None, "empty")

  raw_line = raw_line.replace(" ", "X")

  if "L" in raw_line or "R" in raw_line:
    return (parse_instructions(raw_line), "instructions")
  return (raw_line, "row")

def render(filename=None, instr=None):
  display = "\n".join(canvas)
  if filename:
    if instr:
      display += "\n===\n" + "\n".join([*map(str,instr)])
    with open(filename, "w+", encoding="UTF-8") as output_file:
      output_file.write(display)
  else:
    print(display)

def get_side(target_x, target_y):
  dic = {}
  ids = iter(range(1, 7))
  for y, row in enumerate(canvas):
    for x, cell in enumerate(row):
      if cell != "X":
        val = str((y // SIDE_SIZE * SIDE_SIZE) + (x // SIDE_SIZE))
        if val not in dic:
          dic[val] = str(next(ids))
        if x == target_x and y == target_y:
          return dic[val]
  return None

def get_wrap_pos(from_x, from_y, z, to_d, mirrored):
  def mirror(p):
    return [3,2,1,0][p]
  dic = {}
  ids = iter(range(1, 7))
  top_left = None
  for y, row in enumerate(canvas):
    for x, cell in enumerate(row):
      if cell != "X":
        val = str((y // SIDE_SIZE * SIDE_SIZE) + (x // SIDE_SIZE))
        if val not in dic:
          dic[val] = str(next(ids))
        if dic[val][0] == z:
          top_left = (x, y)
          break
    if top_left:
      break
  x, y = top_left
  if to_d == "N":
    n = from_x // SIDE_SIZE
    x += mirror(n) if mirrored else n
    y += SIDE_SIZE-1
  elif to_d == "S":
    n = from_x // SIDE_SIZE
    x += mirror(n) if mirrored else n
  elif to_d == "W":
    x += SIDE_SIZE-1
    n = from_y // SIDE_SIZE
    y += mirror(n) if mirrored else n
  elif to_d == "E":
    n = from_y // SIDE_SIZE
    y += mirror(n) if mirrored else n
  return x, y

def get_wrap_pos_and_dir(x, y, d):
  side = get_side(x, y)
  side, d, m = next_side[side + d]
  x, y = get_wrap_pos(x, y, side, d, m == "y")
  if canvas[y][x] == "#":
    return (None, None, None)
  return x, y, d

def set_canvas_dimensions():
  mx = max([*map(len, canvas)])
  npos = POS
  for y, r in enumerate(canvas):
    canvas[y] += "X" * (mx - len(r))
    if not npos:
      for x, c in enumerate(r):
        if not npos and c != "X" and c != "#":
          npos = (x, y, "E")
  return npos, (len(canvas[0]), len(canvas))

def draw_at(x, y, glyph, last=None, first=None):
  if last:
    glyph = "e"
  if first:
    glyph = "s"
  row = list(canvas[y])
  row[x] = glyph
  canvas[y] = "".join(row)

def find_wrap_point(x, y, d):
  if d == "N":
    y = DIMS[1] - 1

    while canvas[y][x] == "X":
      y -= 1
  if d == "S":
    y = 0
    while canvas[y][x] == "X":
      y += 1
  if d == "W":
    x = DIMS[0] - 1
    while canvas[y][x] == "X":
      x -= 1
  if d == "E":
    x = 0
    while canvas[y][x] == "X":
      x += 1
  if canvas[y][x] == "#": # Can't wrap
    return (None, None)
  return (x, y)

def get_glyph(d):
  return GLYPHS["ESWN".index(d)]

happened = False

def do_instruction(instr, pos, first=None, last=None):
  global happened

  def restore_prev(x, y):
    if d in "NS":
      y = y + 1 if d == "N" else y - 1
    else:
      x = x + 1 if d == "W" else x - 1
    return (x, y)

  x, y, d = pos

  draw_at(x, y, get_glyph(d), first=first)

  for _ in range(1, instr.distance + 1):
    if d in "NS":
      y = y - 1 if d == "N" else y + 1
    else:
      x = x - 1 if d == "W" else x + 1
    if x == DIMS[0] or y == DIMS[1] or \
       x < 0 or y < 0 or canvas[y][x] == "X":
      px, py = restore_prev(x, y)
      a, b, c = get_wrap_pos_and_dir(px, py, d)
      if (a, b, c) == (None, None, None):
        x, y = restore_prev(x, y)
        break
      happened = True
      x, y, d = a, b, c
    elif canvas[y][x] == "#":
      x, y = restore_prev(x, y)
      break
    draw_at(x, y, get_glyph(d))

  if instr.direction: # `None` delineates the end
    if d == "N":
      d = "E" if instr.direction == "R" else "W"
    elif d == "E":
      d = "S" if instr.direction == "R" else "N"
    elif d == "S":
      d = "W" if instr.direction == "R" else "E"
    else:
      d = "N" if instr.direction == "R" else "S"

  draw_at(x, y, get_glyph(d), last=last)

  return (x, y, d)

def calc_password():
  x, y, d = POS
  row = (y + 1) * 1000
  column = (x + 1) * 4
  facing = DIRS.index(d)
  return row + column + facing

def test_1():
  pos = (11, 5, "E")
  instr = Instruction()
  instr.direction = "E"
  instr.distance = 5
  return [instr], pos

def test_2():
  pos = (10, 11, "S")
  instr = Instruction()
  instr.direction = "S"
  instr.distance = 4
  return [instr], pos

def test_3():
  pos = (6, 4, "N")
  instr = Instruction()
  instr.direction = "N"
  instr.distance = 3
  return [instr], pos

def exec_instructions():
  clip_n = 1
  is_first, is_last = True, False
  npos = POS
  for instr in instructions:
    if instr.direction is None:
      is_last = True
    npos = do_instruction(instr, npos, first=is_first, last=is_last)
    if is_first:
      is_first = False
    render(f"clips/_{str(clip_n).zfill(4)}.txt")
    clip_n += 1
  return npos

def draw_regions():
  counter = 0
  lenf = len(canvas)
  for y, row in enumerate(canvas):
    counter += 1
    if counter % 10:
      print(f"Row {y} of {lenf}")
    for x, _ in enumerate(row):
      side = get_side(x, y)
      if side:
        draw_at(x, y, side)

with open("input2.txt", "r") as file:
#with open("input.txt", "r") as file:
#with open("example.txt", "r", encoding="UTF-8") as file:
  instructions = []
  for line in file.readlines():
    data, kind = parse_line(line.strip("\n"))
    if kind == "empty":
      continue
    if kind == "row":
      canvas.append(data)
    if kind == "instructions":
      instructions += data

  #instructions, POS = test_1()
  POS, DIMS = set_canvas_dimensions()

  #draw_regions()
  POS = exec_instructions()

  render("output.txt")

  print("Password", calc_password(), POS)

"""Notes
  12     1 
  3    234
 45      56
 6       
    
  
  1       6
 4326    412
  5       3

0000111122223333
0000111122223333
0000111122223333
0000111122223333
----------------
4444555566667777
4444555566667777
4444555566667777
4444555566667777
...
"""
