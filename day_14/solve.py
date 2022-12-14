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
  
  #print(xmin, xmax)
  return grid, xmin

def print_grid(grid):
  canvas = ""
  i = 0
  for row in grid:
    canvas += f"{i} {''.join(row)}\n"
    i += 1
  print(canvas)

def drop_sand_loop(grid, xoffset):
  for _ in range(int(sys.argv[1])):
    [x, y], hit = drop_sand(grid, 500-xoffset)
    if hit == "o":
      x, y = settle_sand_at(grid, [x, y])
    grid[y][x] = "o"

def drop_sand(grid, x=0, y=0):
  for row in grid[y:]:
    cell = row[x] 
    if cell == "#":
      return [x, y-1], cell
    if cell == "o":
      return [x, y-1], cell
    y += 1

def no_rocks_above(grid, x, y):
  for _y in range(y, -1, -1):
    if grid[_y][x] == "#":
      return False
  return True

def settle_sand_at(grid, point):
  x, y = point
  i = 1
  last_empty = None
  no_dl = no_dr = False
  try:
    while True:
      # diagonal left
      dl_hit = grid[y+i][x-i]
      # if diagonal left is empty, and below that is a rock, we're good
      if not no_dl and dl_hit == ".":
        [_x, _y], hit = drop_sand(grid, x-i, y+i)
        if hit == "#":
          x, y = [_x, _y]
      if not no_dl and dl_hit == "#":
        no_dl = True

      # diagonal right
      dr_hit = grid[y+i][x+i] 
      # if diagonal right is empty, and below that is a rock, we're good
      if not no_dr and dr_hit == ".":
        [_x, _y], hit = drop_sand(grid, x+i, y+i)
        if hit == "#":
          x, y = [_x, _y]
      if not no_dr and dr_hit == "#":
        no_dr = True
      
      if no_dr and dr_hit == ".":
        last_empty = [x+i, y+i]
      if no_dl and dl_hit == ".":
        last_empty = [x-i, y+i]

      i += 1
  except:
    return [x,y]

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

  drop_sand_loop(grid, xmin)

  print_grid(grid)
