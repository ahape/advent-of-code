grove_indexes = [1000, 2000, 3000]
uid = 0

class Entry():
  def __init__(self, val):
    self.value = int(val)
    self.is_zero = self.value == 0
  def __repr__(self):
    return str(self.value)

def parse_line(line):
  return Entry(line)

def mix(coords, entry, boundary):
  current_i = coords.index(entry)
  i = abs(current_i + entry.value) % boundary

  if entry.value < 0:
    i = boundary - i

  if current_i != i:
    if current_i < i:
      coords.remove(entry)

    coords.insert(i, Entry(entry.value))

    if current_i > i:
      coords.remove(entry)

  return coords

with open("example.txt", "r") as file:
  coords = []
  for line in file.readlines():
    coords.append(parse_line(line.strip()))

  leng, mixed = len(coords), coords[:]
  for entry in coords:
    mixed = mix(mixed, entry, leng-1)
    #print(entry, mixed)

  nums = [x.value for x in mixed]
  to_add = []
  zero_i = [i for i, e in enumerate(mixed) if e.value == 0][0]

  for i in grove_indexes:
    to_add.append(nums[(zero_i + i) % leng])

  print(to_add, sum(to_add))
