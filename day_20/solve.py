grove_indexes = [1000, 2000, 3000]

class Link():
  def __init__(self, val):
    self.value = int(val)
    self.prev = None
    self.next = None
  def __repr__(self):
    return str(self.value)

def mix(link):
  left = link.value < 0
  last = link
  old_prev = link.prev
  old_next = link.next

  if not link.value:
    return

  for _ in range(abs(link.value)):
    last = last.prev if left else last.next

  if left:
    link.next = last
    link.prev = last.prev
    last.prev.next = last.prev = link
  else:
    link.prev = last
    link.next = last.next
    last.next.prev = last.next = link

  old_prev.next = old_next
  old_next.prev = old_prev

def zero_link(coords):
  return [e for i, e in enumerate(coords) if e.value == 0][0]

def grove_coords(coords, zero):
  to_add = []
  cur = zero
  for i in range(max(grove_indexes) + 1):
    if i in grove_indexes:
      to_add.append(cur.value)
    cur = cur.next
  return to_add

def print_coords(coords, link):
  actual = []
  for i in range(len(coords)):
    actual.append(link.value)
    link = link.next
  print("What's there", actual)

def create_linked(file):
  coords = []
  prev = cur = None
  for line in file.readlines():
    cur = Link(line.strip())
    if prev:
      cur.prev = prev
      prev.next = cur
    coords.append(cur)
    prev = cur
  coords[0].prev = cur
  cur.next = prev
  return coords

with open("example.txt", "r") as file:
  coords = create_linked(file)

  for entry in coords:
    mix(entry)
    #print_coords(coords, entry)

  to_add = grove_coords(coords, zero_link(coords))
  summed = sum(to_add)
  assert 3 == summed, (to_add, summed)
  #assert 8764 == summed, (to_add, summed)
