import sys, time

start = time.time()

class LinkedList():
  def __init__(self):
    self.nodes = []
    self.length = 0
    self.first = None
    self.last = None
    self.zero = None

  def __repr__(self):
    return f"[{','.join([*map(str, self.nodes)])}]"

  def add(self, node):
    if node.value == 0:
      self.zero = node
    if not self.first:
      self.first = node
      self.last = node
    self.last.next = node
    self.first.prev = node
    node.list = self
    node.prev = self.last
    node.next = self.first
    self.last = node
    self.nodes.append(node)
    self.length += 1

  def mix(self, rounds):
    for i in range(rounds):
      for node in self.nodes:
        if node != self.zero:
          other = node.get(node.value)
          if node.value < 0:
            node.insert_after(other)
          else:
            node.insert_before(other)
      print(f"Mixed nodes ({i+1})", time.time() - start)

def detach_then_reattach(fn):
  def wrapped(node, *args):
    node.detach()
    ret = fn(node, *args)
    node.attach()
    return ret
  return wrapped

class Node():
  def __init__(self, val, key):
    self.value = int(val) * key
    self.prev = None
    self.next = None
    self.list = None

  def __str__(self):
    return str(self.value)

  def detach(self):
    self.next.prev = self.prev
    self.prev.next = self.next

  def attach(self):
    self.prev.next = self
    self.next.prev = self

  @detach_then_reattach
  def insert_before(self, node):
    self.prev = node
    self.next = node.next

  @detach_then_reattach
  def insert_after(self, node):
    self.next = node
    self.prev = node.prev

  @detach_then_reattach
  def get(self, distance):
    node = self
    move_left = distance < 0
    # `-1` because this node will be detached
    distance = abs(distance) % (node.list.length-1)
    while distance:
      node = node.prev if move_left else node.next
      distance -= 1
    return node

def get_coords(linked):
  return [linked.zero.get(1000).value,
          linked.zero.get(2000).value,
          linked.zero.get(3000).value]

def create_nodes(file, decryption_key=1):
  linked = LinkedList()
  for line in file.readlines():
    linked.add(Node(line.strip(), decryption_key))
  return linked

def parse_args():
  if len(sys.argv) == 3:
    return (int(sys.argv[1]), int(sys.argv[2]))
  return (1,1)

with open("input.txt", "r") as file:
  rounds, decryption_key = parse_args()
  linked = create_nodes(file, decryption_key)
  print("Created nodes", time.time() - start)
  linked.mix(rounds)
  #print(linked)
  coords = get_coords(linked)
  print("Acquired coordinates", time.time() - start)
  print("Answer:", sum(coords))
