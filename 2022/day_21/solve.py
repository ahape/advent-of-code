job_queue = {}

def add_to_queue(monkey, job):
  if monkey not in job_queue:
    job_queue[monkey] = []
  job_queue[monkey].append(job)
  job.waiting_on.append(monkey)

def notify_monkeys_waiting(j):
  monkey, result = j.monkey, j.result
  if monkey not in job_queue:
    return
  for job in job_queue[monkey][:]:
    for i, e in enumerate(job.operation[:]):
      if e == monkey:
        job.operation[i] = result
    if monkey in job.waiting_on:
      job.waiting_on.remove(monkey)
    if job.is_done():
      job.result = compute(*job.operation)
      job_queue[monkey].remove(job)

def compute(*args):
  result = 0
  pending_op = None
  for arg in args:
    num, is_num = try_parse_int(arg)
    if is_num:
      if pending_op:
        if pending_op == "+":
          result += num
        if pending_op == "-":
          result -= num
        if pending_op == "*":
          result *= num
        if pending_op  == "/":
          result //= num
        pending_op = None
      else:
        result += num
    else:
      pending_op = arg
  return result

class Job():
  def __init__(self, monkey, operation):
    self.monkey = monkey
    self.operation = operation
    self.waiting_on = []
    self.result = None
    a, a_is_int = try_parse_int(operation[0])
    if len(operation) == 1:
      if a_is_int:
        self.result = a
    if self.result == None:
      if not a_is_int:
        add_to_queue(a, self)
      _, operator, b = operation
      b, b_is_int = try_parse_int(b)
      if not b_is_int:
        add_to_queue(b, self)

  def is_done(self):
    return not len(self.waiting_on)

def parse_job(line):
  monkey, operation = line.split(":")
  operation = operation.strip().split(" ")
  return Job(monkey, operation)

def order_by_doneness(jobs):
  jobs.sort(key=lambda job: len(job.waiting_on))

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

  order_by_doneness(jobs)
  while not root.is_done():
    for job in jobs:
      if job.is_done():
        notify_monkeys_waiting(job)
    order_by_doneness(jobs)

  print(root.result)
