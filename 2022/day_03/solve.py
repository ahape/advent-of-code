priority = list("_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

"""First solve
with open("input.txt", "r") as file:
  total = 0
  for line in file.readlines():
    line = line.strip()
    half = len(line) // 2
    a, b = set(line[:half]), set(line[half:])
    char = a.intersection(b).pop()
    total += priority.index(char)

print(total)
"""

with open("input.txt", "r") as file:
  total = 0
  lines = [x.strip() for x in file.readlines()]
  chunks = []

  while len(lines):
    chunks.append(lines[:3])
    del lines[:3]

  for chunk in chunks:
    a, b, c = [set(x) for x in chunk]
    char = a.intersection(b).intersection(c).pop()
    total += priority.index(char)

print(total)
