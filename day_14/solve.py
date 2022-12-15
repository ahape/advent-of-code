import sys

class AbyssReachedError(Exception):
  pass

def parse_path(text):
  return [*map(lambda x: [*map(lambda y: int(y), x.split(","))], text.split(" -> "))]

def get_grid_edges(points):
  return (
    # x-min
    min([*map(lambda x: x[0], points)]), 
    # x-max
    max([*map(lambda x: x[0], points)]), 
    # y-min
    min([*map(lambda x: x[1], points)]), 
    # y-max
    max([*map(lambda x: x[1], points)])
  )

def create_grid(path):
  xmin = xmax = ymax = None
  ymin = 0
  for point in path:
    _xmin, _xmax, _ymin, _ymax = get_grid_edges(point)
    if xmin is None or _xmin < xmin:
      xmin = _xmin
    if xmax is None or _xmax > xmax:
      xmax = _xmax
    if ymax is None or _ymax > ymax:
      ymax = _ymax
  grid = []
  for _ in range((ymax - ymin) + 1):
    row = []
    # '3' instead of '1' to make room for the edges that drop into the abyss.
    # 1 for the left edge, 1 for the right
    for _ in range((xmax - xmin) + 3):
      row.append(".")
    grid.append(row)
  
  return grid, xmin - 1

def print_grid(grid):
  canvas = ""
  i = 0
  for row in grid:
    canvas += f"{i} {''.join(row)}\n"
    i += 1
  print(canvas)

def drop_sand_loop(grid, xoffset):
  grains = 0
  try:
    while True:
      [x, y], hit = drop_sand(grid, 500-xoffset)
      if hit == "o":
        x, y = settle_sand(grid, [x, y])
      grid[y][x] = "o"
      grains += 1
  except AbyssReachedError:
    return grains

def drop_sand(grid, x=0, y=0):
  for row in grid[y:]:
    cell = row[x] 
    if cell != ".":
      return [x, y-1], cell
    y += 1
  return [x, y], "~"

def settle_sand_diagonally(grid, point):
  left, right = -1, 1
  [x, y] = orig = point
  can_try_left = can_try_right = True
  
  while can_try_left or can_try_right:
    can_try_left = x + left >= 0 and y + 1 < len(grid) and \
      grid[y + 1][x + left] == "."

    if can_try_left:
      [x, y], hit = drop_sand(grid, x + left, y + 1)
      if hit == "~":
        raise AbyssReachedError
      point = [x, y]
      continue

    can_try_right = x + right < len(grid[0]) and y + 1 < len(grid) and \
      grid[y + 1][x + right] == "."

    if can_try_right:
      [x, y], hit = drop_sand(grid, x + right, y + 1)
      if hit == "~":
        raise AbyssReachedError
      point = [x, y]
      continue

    y += 1; left -= 1; right += 1

  return orig[1] != point[1], point

def settle_sand(grid, point):
  okay, new_spot = settle_sand_diagonally(grid, point)
  if okay:
    return new_spot
  return point

def draw_rocks(path, grid, xoffset):
  last = None
  for point in path:
    x, y = point
    if last:
      lastx, lasty = last
      if x == lastx: # vert
        for _y in range(min(y, lasty), max(y, lasty)):
          grid[_y][x - xoffset] = "#"
      else:
        for _x in range(min(x, lastx), max(x, lastx)):
          grid[y][_x - xoffset] = "#"
    grid[y][x - xoffset] = "#"
    last = point[:]

with open("input.txt") as file:
  paths = []
  for line in file.readlines():
    paths.append(parse_path(line.strip()))

  grid, xmin = create_grid(paths)

  for point in paths:
    draw_rocks(point, grid, xmin)

  #grains = drop_sand_loop(grid, xmin, int(sys.argv[1]))

  grains = drop_sand_loop(grid, xmin)

  print_grid(grid)
  print("Grains landed", grains)
