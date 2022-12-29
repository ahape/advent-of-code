pos = None
canvas = []

class Instruction():
  def __init__(self):
    self.direction = None
    self.distance = 0

  def __repr__(self):
    return f"{self.direction}:{self.distance}"

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
  return instructions

def parse_line(line):
  if not line.strip():
    return (None, "empty")

  line = line.replace(" ", "X")

  if "L" in line or "R" in line:
    return (parse_instructions(line), "instructions")
  return (line, "row")

def render():
  display = "\n".join(canvas)
  print(display)

def set_canvas_dimensions():
  global pos
  _max = max([*map(lambda x: len(x), canvas)])
  for y, line in enumerate(canvas):
    canvas[y] += "X" * (_max - len(line))
    if not pos:
      for x, c in enumerate(line):
        if not pos and c != "X" and c != "#":
          pos = (x, y, "E")

def draw_at(x, y, glyph):
  line = list(canvas[y])
  line[x] = glyph
  canvas[y] = "".join(line)

def find_wrap_point(x, y, d):
  if d == "N":
    y = len(canvas) - 1
    while canvas[y][x] == "X":
      y -= 1
  if d == "S":
    y = 0
    while canvas[y][x] == "X":
      y += 1
  if d == "W":
    x = len(canvas[0]) - 1
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
  return "^v><"["NSEW".index(d)]

def do_instruction(instr):
  global pos
  def restore_prev(x, y):
    if d in "NS":
      y -= 1
    else:
      x -= 1
    return (x, y)
  x, y, d = pos
  print(pos, instr)
  g = get_glyph(d)
  draw_at(x, y, g)
  for n in range(1, instr.distance + 1):
    if d in "NS":
      y += 1
    else:
      x += 1
    if canvas[y][x] == "#":
      x, y = restore_prev(x, y)
      break
    elif canvas[y][x] == "X":
      a, b = find_wrap_point(x, y, d)
      if (a, b) == (None, None):
        x, y = restore_prev(x, y)
        break
      x, y = a, b
    draw_at(x, y, g)

  if d == "N":
    d = "E" if instr.direction == "R" else "W"
  elif d == "E":
    d = "S" if instr.direction == "R" else "N"
  elif d == "S":
    d = "W" if instr.direction == "R" else "E"
  else:
    d = "N" if instr.direction == "R" else "S"

  draw_at(x, y, get_glyph(d))
  pos = (x, y, d)

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

  for instr in instructions:
    do_instruction(instr)

render()
