job_queue = {}
tree_for = None

def add_to_queue(monkey, job):
  if monkey not in job_queue:
    job_queue[monkey] = []
  job_queue[monkey].append(job)
  job.pending.append(monkey)

def resolve(j):
  monkey, value = j.monkey, j.value
  if monkey not in job_queue:
    return
  for job in job_queue[monkey][:]:
    for i, part in enumerate(job.desc[:]):
      job.desc[i] = value if part == monkey else part
    for i, part in enumerate(job.orig[:]):
      if part == monkey:
        first = j.orig[0]
        job.orig[i] = first if len(j.orig)==1 and is_int(first) else j.orig
    if monkey in job.pending:
      job.pending.remove(monkey)
    if job.is_resolved():
      job.value = compute(*job.desc)
      job_queue[monkey].remove(job)

def flatten(arr):
  for item in arr:
    if not isinstance(item, str):
      try:
        yield from flatten(item)
      except TypeError:
        yield item
    else:
      yield item

def compute(*args):
  res = 0
  pending_op = None
  for arg in args:
    num, is_num = try_parse_int(arg)
    if is_num:
      if pending_op:
        if pending_op == "+":
          res += num
        if pending_op == "-":
          res -= num
        if pending_op == "*":
          res *= num
        if pending_op  == "/":
          res //= num
        pending_op = None
      else:
        res += num
    else:
      pending_op = arg
  return res

class Job():
  def __init__(self, monkey, desc):
    self.monkey = monkey
    self.desc = desc
    self.orig = desc[:]
    self.pending = []
    self.value = None
    a, a_is_int = try_parse_int(desc[0])
    if len(desc) == 1:
      if a_is_int:
        self.value = a
    if self.value == None:
      if not a_is_int:
        add_to_queue(a, self)
      _, operator, b = desc
      b, b_is_int = try_parse_int(b)
      if not b_is_int:
        add_to_queue(b, self)

  def __repr__(self):
    return f"\n{self.monkey}:{self.desc} [{'pending' if len(self.pending) else 'resolved'}]"

  def is_resolved(self):
    return not len(self.pending)

def parse_job(line):
  monkey, desc = line.split(":")
  desc = desc.strip().split(" ")
  return Job(monkey, desc)

def try_parse_int(s):
  try:
    return int(s), True
  except ValueError:
    return s, False

def is_int(s):
  return try_parse_int(s)[1]

def simplify(arr):
  out = []
  for e in arr:
    if isinstance(e, list):
      # recurse. May return simplified list or all literals
      out.append(simplify(e))
    else:
      # literal--add to operands
      out.append(e)
  # if our subarr is entirely made of literals, SIMPLIFY
  if not any([isinstance(e, list) for e in out]):
    if "2796" not in out:
      return compute(*out)
  return out

# value = 37154547770460
# goal = 12133706805700
def part_2(value, goal):
  t = 19
  m = [1, 2, 2]
  y = 0
  x = m[y % 3]
  i = 1
  while value > goal:
    if not x:
      value -= 20
      y += 1
      x = m[y % 3]
    else:
      x -= 1
    i += 1
    if i >= t:
      break
  return (i, value)
    
    
  return res
  # Pattern is 2 3 3
  # i    v   x
  # 0 -> 60 (1)
  # 1 -> 40 (2)
  # 2 -> 40 (2)
  # 3 -> 20 (3)
  # 4 -> 20 (3)
  # 5 -> 20 (3)
  # 6 -> 00 (4)
  # 7 -> 00 (4)
  # 8 -> 00 (4)
  # 9 -> 80 (5)
  # 10-> 80 (5)
  # 11-> 60 (6)
  # 12-> 60 (6)
  # 13-> 60 (6)
  # 14-> 40 (7)
  # 15-> 40 (7)
  # 16-> 40 (7)
  # 17-> 20 (8)
  # 18-> 20 (8)
  # 19-> 00 (9)

with open("input.txt", "r") as file:
  jobs = []
  root = None
  for line in file.readlines():
    job = parse_job(line.strip())
    if job.monkey == "root":
      root = job
    jobs.append(job)

  jobs = sorted(jobs, key=lambda job: len(job.pending))
  eq = [j for j in jobs if j.monkey == root.desc[0]][0]
  while not root.is_resolved():
    for job in jobs:
      if job.is_resolved():
        resolve(job)
    jobs = sorted(jobs, key=lambda job: len(job.pending))

  # 0 = -1, 150
  """
  equation = eq.orig
  #equation = [["1", "+", "2"], "+", "1"]
  simplified = simplify(equation)

  print(simplified)
  #print(compute(*equation))
  """

  #assert root.value == 152, root.value
  result = part_2(int(root.desc[0]), int(root.desc[2]))
  print(result)
  print(root.desc)
