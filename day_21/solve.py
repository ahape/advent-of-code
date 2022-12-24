job_queue = {}

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
    if monkey in job.pending:
      job.pending.remove(monkey)
    if job.is_resolved():
      job.value = compute(*job.desc)
      job_queue[monkey].remove(job)

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

  def is_resolved(self):
    return not len(self.pending)

def parse_job(line):
  monkey, desc = line.split(":")
  desc = desc.strip().split(" ")
  return Job(monkey, desc)

def order_by_least_pending(jobs):
  jobs.sort(key=lambda job: len(job.pending))

def try_parse_int(s):
  try:
    return int(s), True
  except ValueError:
    return s, False

with open("input.txt", "r") as file:
  jobs, root = [], None
  for line in file.readlines():
    job = parse_job(line.strip())
    if job.monkey == "root":
      root = job
    jobs.append(job)

  order_by_least_pending(jobs)
  while not root.is_resolved():
    for job in jobs:
      if job.is_resolved():
        resolve(job)
    order_by_least_pending(jobs)

  print(root.value)
