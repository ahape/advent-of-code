class LinkedList():
  def __init__(self):
    self.nodes = []
    self.first = None
    self.last = None
    self.zero = None

  def add(self, node):
    if node.mix_value == 0:
      self.zero = node
    if not self.first:
      self.first = node
      self.last = node
    self.last.next = node
    self.first.prev = node
    node.prev = self.last
    node.next = self.first
    self.last = node
    self.nodes.append(node)

  def mix(self, times):
    for _ in range(times):
      for node in self.nodes:
        if node != self.zero:
          other = node.get(node.mix_value)
          if node.mix_value < 0:
            node.insert_after(other)
          else:
            node.insert_before(other)

def detached(fn):
  def wrapped(*args):
    args[0].detach()
    ret = fn(*args)
    args[0].attach()
    return ret
  return wrapped

class Node():
  def __init__(self, val, key):
    val = int(val)
    self.mix_value = val
    self.value = val * key
    self.prev = None
    self.next = None

  def detach(self):
    self.next.prev = self.prev
    self.prev.next = self.next

  def attach(self):
    self.prev.next = self
    self.next.prev = self

  @detached
  def insert_before(self, node):
    self.prev = node
    self.next = node.next

  @detached
  def insert_after(self, node):
    self.next = node
    self.prev = node.prev

  @detached
  def get(self, distance):
    node = self
    move_left = distance < 0
    while distance:
      node = node.prev if move_left else node.next
      if node == self:
        continue
      distance += (1 if move_left else -1)
    return node

def get_coords(nodes, zero):
  one = zero.get(1000)
  two = one.get(1000)
  three = two.get(1000)
  return [one.value, two.value, three.value]

def create_nodes(file, decryption_key=1):
  linked = LinkedList()
  for line in file.readlines():
    linked.add(Node(line.strip(), decryption_key))
  return linked

with open("input.txt", "r") as file:
  linked = create_nodes(file)
  linked.mix(1)

  coords = get_coords(linked.nodes, linked.zero)

  print(sum(coords))
