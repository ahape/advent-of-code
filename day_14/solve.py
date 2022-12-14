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
  for _ in range(24):
    [x, y], hit = drop_sand(grid, xoffset)
    if hit == "o":
      x, y = settle_sand_at(grid, [x,y], hit)
    grid[y][x] = "o"

def drop_sand(grid, xoffset):
  x, y = 500 - xoffset, 0
  for row in grid:
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

def settle_sand_at(grid, point, hit):
  x, y = point
  j = 0
  i = 1
  last_empty = None
  try:
    while True:
      # diagonal left
      dl_hit = grid[y+i][x-i]
      if dl_hit == "." and grid[y+i+1][x-i] == "#":
        return [x-i, y+i]
      if dl_hit == "#" and no_rocks_above(grid, x-i, y+i):
        return [x-j, y+j]
      # diagonal right
      dr_hit = grid[y+i][x+i] 
      if dr_hit == "." and grid[y+i+1][x+i] == "#":
        return [x+i, y+i]
      if dr_hit == "#" and no_rocks_above(grid, x+i, y+i):
        return [x+j, y+j]
      if dr_hit == ".":
        last_empty = [x+i, y+i]
      if dl_hit == ".":
        last_empty = [x-i, y+i]
      """
      if dr_hit == ".":
        if grid[y+j][x+j] == "#" and no_rocks_above(grid, x+i, y+i):
          return [x+i, y+i]
        elif grid[y+i][x+j] == "o":
          return [x+i, y+i]
      if dl_hit == "#" and \
          not no_rocks_above(grid, x-i, y+i) and \
          dr_hit == "#" and \
          not no_rocks_above(grid, x+i, y+i):
        return [x, y]
      """
      j = i
      i += 1
  except:
    return last_empty or [x,y]

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
