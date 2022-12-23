job_queue = {}

def add_to_queue(monkey, job):
  if monkey not in job_queue:
    job_queue[monkey] = []
  job_queue[monkey].append(job)
  job.pending.append(monkey)

def resolve(monkey, value):
  for jobs in job_queue[monkey]:
    for i, part in enumerate(job.desc[:]):
      job.desc[i] = value if part == monkey else part
    remove_from_queue(monkey, job)

def remove_from_queue(monkey, job):
  job_queue[monkey].remove(job)
  job.pending.append(monkey)

class Job():
  def __init__(self, desc):
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
    return f"{self.desc} [{'pending' if len(self.pending) else 'resolved'}]"

def parse_line(line):
  monkey, desc = line.split(":")
  desc = desc.strip().split(" ")
  return (monkey, Job(desc))

def try_parse_int(s):
  try:
    return int(s), True
  except ValueError:
    return None, False

with open("example.txt", "r") as file:
  lines = []
  for line in file.readlines():
    lines.append(parse_line(line.strip()))

  print(lines)
