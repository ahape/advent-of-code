import sys

LOSE, DRAW, WIN = 0, 3, 6
ABC = ["A", "B", "C"]
XYZ = ["X", "Y", "Z"]
VAL = { "X": 1, "Y": 2, "Z": 3 }

def get_result(them, you):
  them = ABC.index(them)
  you = XYZ.index(you)
  res = you - them
  return WIN if res in [1, -2] else DRAW if not res else LOSE

def decode(them, you):
  them = ABC.index(them)
  you = XYZ.index(you)
  res = you * 3
  n = 1 if res == WIN else 0 if res == DRAW else 2
  return XYZ[(them + n) % len(XYZ)]

with open("input.txt", "r") as file:
  total = 0
  for line in file.readlines():
    them, you = line.strip().split(" ")
    if len(sys.argv) > 1:
      you = decode(them, you)
    total += (get_result(them, you) + VAL[you])

print(total)




