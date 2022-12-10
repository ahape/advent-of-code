def get_op_cycles(instr):
  return 1 if instr == "noop" else 2

def get_instruction(line):
  if line == "noop":
    return "noop", None
  parts = line.split(" ")
  return parts[0], int(parts[1])

def should_do_signal_strength_check():
  return cycles==20 or not (cycles-20) % crt_width

def signal_strength():
  return X * cycles

def is_sprite_visible():
  return abs(X - crt_line_index()) < 2

def crt_line_index():
  return (cycles-1) % crt_width

cycles = X = 1
signal_strengths = []
crt_width = 40
crt_display = ""

with open("input.txt") as file:
  for line in file.readlines():
    line = line.strip()
    op, val = get_instruction(line)
    op_cycles = get_op_cycles(op)
    for _ in range(op_cycles):
      # Part 1
      if should_do_signal_strength_check():
        signal_strengths.append(signal_strength())

      # Part 2
      if not crt_line_index():
        crt_display += "\n"
      crt_display += "#" if is_sprite_visible() else "."

      cycles += 1
    if op == "addx":
      X += val

print(sum(signal_strengths))
print(crt_display)
