with open("input.txt") as f:
  sum, totals = 0, []
  for row in f.readlines():
    row = row.strip()
    if not row:
      totals.append(sum)
      sum = 0
    else:
      sum += int(row)

most = max(totals)
print("Part 1 answer", most)

sum = most
totals.remove(most)

for _ in range(2):
  most = max(totals)
  sum += most
  totals.remove(most)

print("Part 2 answer", sum)
