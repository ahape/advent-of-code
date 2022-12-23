grove_indexes = [1000, 2000, 3000]

class Node():
  def __init__(self, val):
    self.value = int(val)
    self.prev = None
    self.next = None

  def detach(self):
    self.next.prev = self.prev
    self.prev.next = self.next

  def insert_before(self, node):
    self.prev = node
    self.next = node.next
    node.next.prev = node.next = self

  def insert_after(self, node):
    self.next = node
    self.prev = node.prev
    node.prev.next = node.prev = self

  def get_node(self, distance):
    node = self
    move_left = distance < 0
    while distance:
      node = node.prev if move_left else node.next
      if node == self:
        continue
      distance += (1 if move_left else -1)
    return node

  def __repr__(self):
    return str(self.value)

def mix(node):
  if node.value:
    node.detach()
    other = node.get_node(node.value)
    if node.value < 0:
      node.insert_after(other)
    else:
      node.insert_before(other)

def zero_node(node):
  while node.value != 0:
    node = node.next
  return node

def grove_coords(nodes, zero):
  to_add = []
  cur = zero
  for i in range(max(grove_indexes) + 1):
    if i in grove_indexes:
      to_add.append(cur.value)
    cur = cur.next
  return to_add

def print_coords(nodes, node):
  actual = []
  for i in range(len(nodes)):
    actual.append(node.value)
    node = node.next
  print("What's there", actual)

def create_nodes(file):
  nodes = []
  prev = cur = None
  for line in file.readlines():
    cur = Node(line.strip())
    if prev:
      cur.prev = prev
      prev.next = cur
    nodes.append(cur)
    prev = cur
  nodes[0].prev = cur
  cur.next = prev
  return nodes

with open("input.txt", "r") as file:
  nodes = create_nodes(file)

  for entry in nodes:
    mix(entry)
    #print_coords(nodes, entry)

  to_add = grove_coords(nodes, zero_node(nodes[0]))
  summed = sum(to_add)
  #assert 3 == summed, (to_add, summed)
  assert 8764 == summed, (to_add, summed)
