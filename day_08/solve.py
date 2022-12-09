forest = [] # A matrix of ints
col_len = row_len = 0
visible = max_score = 0

# Produce an iterable that walks backwards or forwards depending on args
def get_range(horiz, left_or_up, i):
  start, end, inc = (i - 1, -1, -1) if left_or_up else (i + 1, (col_len if horiz else row_len), 1)
  return range(start, end, inc)

def check_left_right(row, col, val, left):
  for c in get_range(True, left, col):
    if forest[row][c] >= val:
      return False
  return True

def check_up_down(row, col, val, up):
  for r in get_range(False, up, row):
    if forest[r][col] >= val:
      return False
  return True

def score_left_right(row, col, val, left):
  score = 0
  for c in get_range(True, left, col):
    score += 1
    if forest[row][c] >= val:
      break
  return score

def score_up_down(row, col, val, up):
  score = 0
  for r in get_range(False, up, row):
    score += 1
    if forest[r][col] >= val:
      break
  return score

def check_visible(row, col):
  tree = forest[row][col]
  return check_left_right(row, col, tree, True) or \
    check_left_right(row, col, tree, False) or \
    check_up_down(row, col, tree, True) or \
    check_up_down(row, col, tree, False)

def get_score(row, col):
  tree = forest[row][col]
  return score_left_right(row, col, tree, True) * \
    score_left_right(row, col, tree, False) * \
    score_up_down(row, col, tree, True) * \
    score_up_down(row, col, tree, False)

# Initialize forest, col_len, row_len
with open("input.txt", "r") as file:
  for row in file.readlines():
    row = [int(x) for x in row.strip()]
    if not col_len:
      col_len = len(row)
    forest.append(row)
  row_len = len(forest)

# Part one
for r in range(row_len):
  for c in range(col_len):
    if check_visible(r, c):
      visible += 1

# Part two
for r in range(row_len):
  for c in range(col_len):
    score = get_score(r, c)
    if score > max_score:
      max_score = score

print(visible)
print(max_score)
