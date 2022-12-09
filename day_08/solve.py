grid = []
cols = rows = 0
visible = max_score = 0

def get_range(horiz, left_or_up, i):
  start, end, inc = (i - 1, -1, -1) if left_or_up else (i + 1, (cols if horiz else rows), 1)
  return range(start, end, inc)

def check_lr(row, col, val, left):
  for c in get_range(True, left, col):
    if grid[row][c] >= val:
      return False
  return True

def check_ud(row, col, val, up):
  for r in get_range(False, up, row):
    if grid[r][col] >= val:
      return False
  return True

def score_lr(row, col, val, left):
  score = 0
  for c in get_range(True, left, col):
    score += 1
    if grid[row][c] >= val:
      break
  return score

def score_ud(row, col, val, up):
  score = 0
  for r in get_range(False, up, row):
    score += 1
    if grid[r][col] >= val:
      break
  return score

def check_visible(row, col):
  tree = grid[row][col]
  return check_lr(row, col, tree, True) or \
    check_lr(row, col, tree, False) or \
    check_ud(row, col, tree, True) or \
    check_ud(row, col, tree, False)

def get_score(row, col):
  tree = grid[row][col]
  return score_lr(row, col, tree, True) * \
    score_lr(row, col, tree, False) * \
    score_ud(row, col, tree, True) * \
    score_ud(row, col, tree, False)

# Initialize grid, cols, rows
with open("input.txt", "r") as file:
  for row in file.readlines():
    row = [int(x) for x in row.strip()]
    if not cols:
      cols = len(row)
    grid.append(row)
  rows = len(grid)

# Part one
for r in range(rows):
  for c in range(cols):
    if check_visible(r, c):
      visible += 1

# Part two
for r in range(rows):
  for c in range(cols):
    score = get_score(r, c)
    if score > max_score:
      max_score = score

print(visible)
print(max_score)
