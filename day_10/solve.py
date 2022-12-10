cycles = X = 1
signal_strengths = []
crt_width = 40
crt_display = ""

def get_op_cycles(instr):
  return 1 if instr == "noop" else 2

def get_instructions(file):
  instructions = []
  for line in file.readlines():
    line = line.strip()
    if line == "noop":
      instructions.append(("noop", None))
    else:
      parts = line.split(" ")
      instructions.append((parts[0], int(parts[1])))
  return instructions

def should_do_signal_strength_check():
  return cycles==20 or not (cycles-20) % crt_width

def signal_strength():
  return X * cycles

def is_sprite_visible():
  return abs(X - crt_line_index()) < 2

def crt_line_index():
  return (cycles-1) % crt_width

def exec_instruction(op, val):
  global X
  if op == "addx":
    X += val

def exec_cycle():
  global cycles, crt_display

  # Part 1
  if should_do_signal_strength_check():
    signal_strengths.append(signal_strength())

  # Part 2
  if not crt_line_index():
    crt_display += "\n"
  crt_display += "#" if is_sprite_visible() else "."

  cycles += 1

# Main()
with open("input.txt") as file:
  for op, val in get_instructions(file):
    for cycle in range(get_op_cycles(op)):
      exec_cycle()
    exec_instruction(op, val)

print(sum(signal_strengths))
print(crt_display)
