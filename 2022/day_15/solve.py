import re

sensor_beacon_rx = re.compile(r"(-?\d+)")
xoffset = yoffset = 0

# Returns sensor x, sensor y, beacon x, beacon y
def parse_line(line):
  coords = re.findall(sensor_beacon_rx, line)
  return [*map(int, coords)]

def parse_file(file):
  sensors = []
  beacons = []
  for line in file.readlines():
    (sx, sy, bx, by) = parse_line(line.strip())
    sensors.append((sx, sy))
    beacons.append((bx, by))
  return sensors, beacons

def offset(x, y):
  return (x + xoffset), (y + yoffset)

def plot_sensors_and_beacons(sensors, beacons):
  for x, y in sensors:
    ox, oy = offset(x, y)
    graph[oy][ox] = "S"
  for x, y in beacons:
    ox, oy = offset(x, y)
    graph[oy][ox] = "B"

def create_graph(sensors, beacons):
  global xoffset, yoffset
  xlist = [*map(lambda xy: xy[0], sensors + beacons)]
  ylist = [*map(lambda xy: xy[1], sensors + beacons)]
  xmin, xmax, ymin, ymax = min(xlist), max(xlist), min(ylist), max(ylist)
  xrange, yrange = xmax - xmin, ymax - ymin
  xoffset, yoffset = abs(xmin), abs(ymin)
  return [["."] * (xrange + 1) for _ in range(yrange + 1)]

def expand_graph(graph):
  global xoffset, yoffset
  xoffset += 1; yoffset += 1
  for row in graph:
    row.insert(0, ".")
    row.append(".")
  empty = ["."] * len(graph[0])
  graph.insert(0, empty)
  graph.append(empty[:])

def plot_empty_zones(graph, sensor):
  def within_graph_bounds(_x, _y): 
    return _x >= 0 and _y >= 0 and _x < len(graph[0]) and _y < len(graph)

  def get_checks_for_point(point):
    px, py = point
    return (px-1, py),(px+1, py),(px, py-1),(px, py+1)

  def next_checks(current_chx):
    chx = []
    for c in current_chx:
      chx += get_checks_for_point(c)
    return chx

  beacon_detected = False
  checks = [sensor]

  while not beacon_detected:
    add_after_expand = []
    checks = next_checks(checks)

    for (x, y) in checks:
      ox, oy = offset(x, y)
      if not within_graph_bounds(ox, oy):
        add_after_expand.append((x, y))
        continue
      terrain = graph[oy][ox]
      if terrain == "B":
        beacon_detected = True
      elif terrain == ".":
        graph[oy][ox] = "#"

    if len(add_after_expand):
      expand_graph(graph)
      for x, y in [offset(x, y) for x, y in add_after_expand]:
        graph[y][x] = "#"
      add_after_expand = []

def print_graph(graph):
  canvas = ""
  for i in range(len(graph)):
    canvas += f"{str(i).zfill(2)} {''.join(graph[i])}\n"
  print(canvas)

with open("example.txt") as file:
  sensors, beacons = parse_file(file)
  graph = create_graph(sensors, beacons)
  plot_sensors_and_beacons(sensors, beacons)
  for sensor in sensors:
    plot_empty_zones(graph, sensor)
  print_graph(graph)
