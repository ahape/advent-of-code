import sys

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
    for _ in range((xmax - xmin) + 1):
      row.append(".")
    grid.append(row)
  
  return grid, xmin

def print_grid(grid):
  canvas = ""
  i = 0
  for row in grid:
    canvas += f"{i} {''.join(row)}\n"
    i += 1
  print(canvas)

def drop_sand_loop(grid, xoffset, grains):
  for _ in range(grains):
    [x, y], hit = drop_sand(grid, 500-xoffset)
    if hit == "o":
      x, y = settle_sand(grid, [x, y])
    grid[y][x] = "o"

def drop_sand(grid, x=0, y=0):
  for row in grid[y:]:
    cell = row[x] 
    if cell != ".":
      return [x, y-1], cell
    y += 1

def settle_sand_diagonally(grid, point, left):
  xchange = -1 if left else 1
  x, y = point[0] + xchange, point[1] + 1
  okay_spot = None

  try:
    while grid[y][x] == ".": 
      [x, y], hit = drop_sand(grid, x, y)
      if grid[y][x] == ".":
        okay_spot = [x, y]
      x += xchange
      y += 1
  except:
    pass

  return bool(okay_spot), okay_spot or point

def settle_sand(grid, point):
  settled_left, new_left_spot = settle_sand_diagonally(grid, point, True)
  settled_right, new_right_spot = settle_sand_diagonally(grid, point, False)

  if settled_left:
    return new_left_spot

  if settled_right:
    return new_right_spot

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

with open("example.txt") as file:
  paths = []
  for line in file.readlines():
    paths.append(parse_path(line.strip()))

  grid, xmin = create_grid(paths)

  for point in paths:
    draw_rocks(point, grid, xmin)

  drop_sand_loop(grid, xmin, int(sys.argv[1]))

  print_grid(grid)