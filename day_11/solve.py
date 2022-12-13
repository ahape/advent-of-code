class Monkey():
  def __init__(self, number):
    self.name = f"Monkey {number}"
    self.inspections = 0
    self.items = []
    self.operation = None
    self.test = None
    self.handle_true = None
    self.handle_false = None

monkeys = []
starting_items_flag = "Starting items: "
operation_flag = "Operation: "

def parse_monkey_index(text):
  return int(text[:-1].split(" ")[1])

def parse_items(text):
  return [int(n) for n in text[len(starting_items_flag):].split(", ")]

def parse_operator(operator, old):
  if operator == "old":
    return old
  return int(operator)

def parse_operation(text):
  operation = text[len(operation_flag):].split(" ")
  _, _, v1, op, v2 = operation
  if op == "+":
    return lambda old: (parse_operator(v1, old) + parse_operator(v2, old)) // 3
  if op == "-":
    return lambda old: (parse_operator(v1, old) - parse_operator(v2, old)) // 3
  if op == "*":
    return lambda old: (parse_operator(v1, old) * parse_operator(v2, old)) // 3
  if op == "/":
    return lambda old: (parse_operator(v1, old) // parse_operator(v2, old)) // 3

def parse_test(text):
  # assuming div by
  item = int(text.split(" ")[-1])
  return lambda x: not(x % item)

def parse_receiver(text):
  return int(text.split(" ")[-1])

def do_throw(monkey, receiver, item):
  monkeys[receiver].items.append(item)
  monkey.items.remove(item)

def parse_if(text, monkey):
  receiver = parse_receiver(text)
  return lambda item: do_throw(monkey, receiver, item)

def parse_line(line, index):
  if len(monkeys):
    monkey = monkeys[index]

  if line.startswith("Monkey "):
    index = parse_monkey_index(line)
    monkeys.append(Monkey(index))
  elif line.startswith(starting_items_flag):
    monkey.items = parse_items(line)
  elif line.startswith(operation_flag):
    monkey.operation = parse_operation(line)
  elif line.startswith("Test: "):
    monkey.test = parse_test(line)
  elif line.startswith("If true: "):
    monkey.handle_true = parse_if(line, monkey)
  elif line.startswith("If false: "):
    monkey.handle_false = parse_if(line, monkey)
  return index

def do_round(round_number):
  print(f"- Round {round_number} -")
  for monkey in monkeys:
    monkey.items = [monkey.operation(item) for item in monkey.items]
    items = monkey.items[:]
    for item in items:
      monkey.inspections += 1
      if monkey.test(item):
        monkey.handle_true(item)
      else:
        monkey.handle_false(item)
  for monkey in monkeys:
    print(monkey.name, monkey.inspections, monkey.items)

def get_monkey_business(top_x):
  most_inspections = sorted(monkeys[:], key=lambda x: x.inspections, reverse=True)[:top_x]
  monkey_business = 1
  for monkey in most_inspections:
    monkey_business *= monkey.inspections
  return monkey_business

def parse_input():
  index = 0
  for line in file.readlines():
    index = parse_line(line.strip(), index)

with open("input.txt") as file:
  parse_input()

  # Part 1:
  for n in range(1, 21):
    do_round(n)

  print("Monkey_business", get_monkey_business(2))
