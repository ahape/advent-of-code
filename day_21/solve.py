job_queue = {}

def add_to_queue(monkey, job):
  if monkey not in job_queue:
    job_queue[monkey] = []
  job_queue[monkey].append(job)
  job.pending.append(monkey)

def resolve(monkey, value):
  if monkey not in job_queue:
    return
  for job in job_queue[monkey][:]:
    for i, part in enumerate(job.desc[:]):
      job.desc[i] = value if part == monkey else part
    if monkey in job.pending:
      job.pending.remove(monkey)
    if job.is_resolved():
      job.compute()
      job_queue[monkey].remove(job)

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
      else:
        raise "Unexpected unary"
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

  def compute(self):
    a, operator, b = self.desc
    if operator == "+":
      self.value = int(a) + int(b)
    if operator == "-":
      self.value = int(a) - int(b)
    if operator == "*":
      self.value = int(a) * int(b)
    if operator == "/":
      self.value = int(a) // int(b)

def parse_job(line):
  monkey, desc = line.split(":")
  desc = desc.strip().split(" ")
  return Job(monkey, desc)

def try_parse_int(s):
  try:
    return int(s), True
  except ValueError:
    return s, False

with open("input.txt", "r") as file:
  jobs = []
  for line in file.readlines():
    jobs.append(parse_job(line.strip()))

  jobs = sorted(jobs, key=lambda job: len(job.pending))
  root = None
  while not root:
    for job in jobs:
      if job.is_resolved():
        if job.monkey == "root":
          root = job
        resolve(job.monkey, job.value)
    jobs = sorted(jobs, key=lambda job: len(job.pending))

  # 0 = -1, 150
  print(root.desc)
  #assert root.value == 152, root.value
  print(root.value)
