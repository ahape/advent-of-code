pos = None
canvas = []
glyphs = ">v<^"
dirs = "ESWN"
dims = (0, 0)
side_size = 4

next_side = {}

if side_size == 4:
  next_side["1N"] = "2N"
  next_side["1E"] = "6W"
  next_side["1W"] = "3S"
  next_side["2N"] = "1S"
  next_side["2S"] = "5N"
  next_side["2W"] = "6N"
  next_side["3N"] = "1E"
  next_side["3S"] = "5E"
  next_side["4E"] = "6S"
  next_side["5S"] = "2N"
  next_side["5W"] = "3N"
  next_side["6N"] = "4W"
  next_side["6S"] = "2W"
  next_side["6E"] = "1W"
else:
  pass

is_last = False

class Instruction():
  def __init__(self):
    self.direction = None
    self.distance = 0

  def __str__(self):
    return f"{self.distance}:{self.direction}"

  def __repr__(self):
    return self.__str__()

def parse_instructions(instructions_raw):
  instructions = []
  instruction = Instruction()
  distance = ""
  for e in instructions_raw:
    if e == "L" or e == "R":
      instruction.distance += int(distance)
      distance = ""
      instruction.direction = e
      instructions.append(instruction)
      instruction = Instruction()
    else:
      distance += e
  instruction.direction = None
  instruction.distance = int(distance)
  instructions.append(instruction)
  return instructions

def parse_line(line):
  if not line.strip():
    return (None, "empty")

  line = line.replace(" ", "X")

  if "L" in line or "R" in line:
    return (parse_instructions(line), "instructions")
  return (line, "row")

def render(file=None, instr=None):
  display = "\n".join(canvas)
  if file:
    if instr:
      display += "\n===\n" + "\n".join([*map(str,instr)])
    open(file, "w+").write(display)
  else:
    print(display)

"""
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

def get_side(target_x, target_y):
  dic = {}
  ids = iter(range(1, 7))
  for y, row in enumerate(canvas):
    for x, cell in enumerate(row):
      if cell != "X":
        val = str((y // side_size * side_size) + (x // side_size))
        if val not in dic:
          dic[val] = str(next(ids))
        if x == target_x and y == target_y:
          return dic[val]

def get_wrap_pos(from_x, from_y, z, to_d):
  def mirror(p):
    i = [0,1,2,3].index(p)
    return [3,2,1,0][p]

  dic = {}
  ids = iter(range(1, 7))
  top_left = None
  for y, row in enumerate(canvas):
    for x, cell in enumerate(row):
      if cell != "X":
        val = str((y // side_size * side_size) + (x // side_size))
        if val not in dic:
          dic[val] = str(next(ids))
        if dic[val][0] == z:
          top_left = (x, y)
          break
    if top_left:
      break
  x, y = top_left
  if to_d == "N":
    x += mirror(from_x // side_size)
    y += side_size-1
  elif to_d == "S":
    x += from_x // side_size
  elif to_d == "W":
    x += side_size-1
    y += from_y // side_size
  elif to_d == "E":
    y += mirror(from_y // side_size)
  return x, y

def get_wrap_pos_and_dir(x, y, d):
  side = get_side(x, y)
  side, d = next_side[side + d]
  x, y = get_wrap_pos(x, y, side, d)
  if canvas[y][x] == "#":
    return (None, None, None)
  return x, y, d

def set_canvas_dimensions():
  global pos, dims
  _max = max([*map(lambda x: len(x), canvas)])
  for y, line in enumerate(canvas):
    canvas[y] += "X" * (_max - len(line))
    if not pos:
      for x, c in enumerate(line):
        if not pos and c != "X" and c != "#":
          pos = (x, y, "E")
  dims = (len(canvas[0]), len(canvas))

def draw_at(x, y, glyph):
  if is_last:
    glyph = "WENS"["<>^v".index(glyph)]
  line = list(canvas[y])
  line[x] = glyph
  canvas[y] = "".join(line)

def find_wrap_point(x, y, d):
  if d == "N":
    y = dims[1] - 1
    while canvas[y][x] == "X":
      y -= 1
  if d == "S":
    y = 0
    while canvas[y][x] == "X":
      y += 1
  if d == "W":
    x = dims[0] - 1
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
  return glyphs["ESWN".index(d)]

def do_instruction(instr):
  global pos
  def restore_prev(x, y):
    if d in "NS":
      y = y + 1 if d == "N" else y - 1
    else:
      x = x + 1 if d == "W" else x - 1
    return (x, y)
  x, y, d = pos
  #print(pos, instr)
  draw_at(x, y, get_glyph(d))
  for n in range(1, instr.distance + 1):
    if d in "NS":
      y = y - 1 if d == "N" else y + 1
    else:
      x = x - 1 if d == "W" else x + 1
    if x == dims[0] or y == dims[1] or \
       x < 0 or y < 0 or canvas[y][x] == "X":
      px, py = restore_prev(x, y)
      a, b, c = get_wrap_pos_and_dir(px, py, d)
      if (a, b, c) == (None, None, None):
        x, y = restore_prev(x, y)
        break
      x, y, d = a, b, c
    elif canvas[y][x] == "#":
      x, y = restore_prev(x, y)
      break
    draw_at(x, y, get_glyph(d))

  if instr.direction: # `None` delineates the end
    """
    if d == "N":
      d = "E" if instr.direction == "R" else "W"
    elif d == "E":
      d = "S" if instr.direction == "R" else "N"
    elif d == "S":
      d = "W" if instr.direction == "R" else "E"
    else:
      d = "N" if instr.direction == "R" else "S"
    """

  draw_at(x, y, get_glyph(d))
  pos = (x, y, d)

def calc_password():
  x, y, d = pos
  row = (y + 1) * 1000
  column = (x + 1) * 4
  facing = dirs.index(d)
  return row + column + facing

def test_1():
  global pos
  pos = (11, 5, "E")
  instr = Instruction()
  instr.direction = "E"
  instr.distance = 5
  do_instruction(instr)

def test_2():
  global pos
  pos = (10, 11, "S")
  instr = Instruction()
  instr.direction = "S"
  instr.distance = 4
  do_instruction(instr)

def test_3():
  global pos
  pos = (6, 4, "N")
  instr = Instruction()
  instr.direction = "N"
  instr.distance = 3
  do_instruction(instr)

#with open("input2.txt", "r") as file:
#with open("input.txt", "r") as file:
with open("example.txt", "r") as file:
  instructions = []
  for line in file.readlines():
    data, kind = parse_line(line.strip("\n"))
    if kind == "empty":
      continue
    if kind == "row":
      canvas.append(data)
    if kind == "instructions":
      instructions += data

  set_canvas_dimensions()

  """
  12     1 
  3    234
 45      56
 6       
    
  
  1       6
 4326    412
  5       3
  """
  # testing
  """
  for y, row in enumerate(canvas):
    for x, cell in enumerate(row):
      side = get_side(x, y)
      if side:
        draw_at(x, y, side)
  """
  test_3()

  """
  for instr in instructions:
    if instr.direction == None:
      is_last = True
    do_instruction(instr)
render("output.txt", instructions)
print("Password", calc_password(), pos)
  """

render()
