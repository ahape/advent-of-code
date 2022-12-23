job_queue = {}

class Job():
  def __init__(self, job):
    self.job = job
    self.pending = []
    self.value = None
    a, a_is_int = try_parse_int(job[0])
    if len(job) == 1:
      if a_is_int:
        self.value = a
      else:
        raise "Unexpected unary"
    if self.value == None:
      if not a_is_int:
        self.pending.append(a)
      _, operator, b = job
      b, b_is_int = try_parse_int(b)
      if not b_is_int:
        self.pending.append(b)

  def __repr__(self):
    return f"{self.job} [{'pending' if len(self.pending) else 'resolved'}]"

def parse_line(line):
  monkey, job = line.split(":")
  job = job.strip()
  return (monkey, Job(job.split(" ")))

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
