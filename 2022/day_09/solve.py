# NOTE: y, x

def next_tail(tail, head):
  # if within adjacent matrix
  y, x = tail
  diffy, diffx = head[0] - y, head[1] - x
  # Don't move at all if within one cell away
  if abs(diffy) <= 1 and abs(diffx) <= 1:
    return tail
  if abs(diffx) > 1:
    x += -1 if diffx < 0 else 1
    if abs(diffy):
      y += -1 if diffy < 0 else 1
  elif abs(diffy) > 1:
    y += -1 if diffy < 0 else 1
    if abs(diffx):
      x += -1 if diffx < 0 else 1
  return y, x

def next_head(head, direc):
  if direc == "U":
    return (head[0] - 1, head[1])
  if direc == "D":
    return (head[0] + 1, head[1])
  if direc == "L":
    return (head[0], head[1] - 1)
  if direc == "R":
    return (head[0], head[1] + 1)

placements = set()
knots = 9

def do_move(head, tails, move):
  direc, spaces = move
  #print("==", direc, spaces, "==")
  for _ in range(int(spaces)):
    head = next_head(head, direc)
    prev = head
    updated = []
    for tail in tails:
      tail = next_tail(tail, prev)
      prev = tail
      updated.append(tail)
    tails = updated
    placements.add(tails[-1])
    #paint(head, tails)
  return head, tails

canvas = (200,200)
def paint(head, tails):
  grid = []
  pl = list(placements)
  xs = [*map(lambda yx: yx[1], [head] + tails)]
  ys = [*map(lambda yx: yx[0], [head] + tails)]
  placementxs = [*map(lambda yx: yx[1], pl)]
  placementys = [*map(lambda yx: yx[0], pl)]
  xmin = min(xs + placementxs)
  xmax = max(xs + placementxs)
  ymin = min(ys + placementys)
  ymax = max(ys + placementys)
  width = xmax - xmin + 1
  height = ymax - ymin + 1
  for y in range(height):
    grid.append(["."] * width)
  for y, x in pl:
    grid[y - ymin][x - xmin] = "#"

  coords = zip(ys, xs)
  for y,x in coords:
    grid[y - ymin][x - xmin] = "T"
  grid[head[0] - ymin][head[1] - xmin] = "H"
  for r in grid:
    print("".join(r))
  print()

with open("input.txt", "r") as file:
  head = (canvas[0]//2,canvas[1]//2)
  tails = [*map(lambda _: head, range(knots))]
  #paint(head, tails)
  for line in file.readlines():
    line = line.strip()
    move = line.split(" ")
    head, tails = do_move(head, tails, move)
  paint(head, tails)

# Part one
print(len(list(placements)))
