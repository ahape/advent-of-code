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
  if entry.is_zero:
    return coords
  i = abs(coords.index(entry) + entry.value) % boundary
  if entry.value < 0:
    i = boundary - i
  coords.remove(entry)
  coords.insert(i, entry)
  return coords

with open("before.txt", "r") as file:
  coords = []
  for line in file.readlines():
    coords.append(parse_line(line.strip()))

  # Need to know where something traveled

  i, leng, mixed = 0, len(coords), coords[:]
  for entry in coords:
    mixed = mix(mixed, entry, leng-1)
    break
    #print(entry, mixed)
    i += 1

  nums = [x.value for x in mixed]
  print(len(nums), min(nums), max(nums))
  to_add = []
  zero_i = [i for i, e in enumerate(mixed) if e.is_zero][0]

  for i in range(max(grove_indexes) + 1):
    if i in grove_indexes:
      to_add.append(nums[(zero_i + i) % leng])

  with open("after.txt", "w+") as output:
    output.write("\n".join([str(x) for x in nums]))
  #assert(tuple(mixed) == (1, 2, -3, 4, 0, 3, -2))
  #print(sum(to_add))
