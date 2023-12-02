forest = [] # A matrix of ints
col_len = row_len = 0
visible = max_score = 0

def get_trees(direc, row, col):
  horiz = direc == "L" or direc == "R"
  left_or_up = direc == "L" or direc == "U"
  a = row if direc == "U" or direc == "D" else col
  b = col if direc == "U" or direc == "D" else row
  start, end, inc = (a-1, -1, -1) if left_or_up else (a+1, (col_len if horiz else row_len), 1)
  return [forest[b if horiz else c][c if horiz else b] for c in range(start, end, inc)]

def visible_for_direction(direc, row, col, tree):
  trees = get_trees(direc, row, col)
  return all(t < tree for t in trees)

def score_for_direction(direc, row, col, tree):
  trees = get_trees(direc, row, col)
  vis = 0
  for t in trees:
    vis += 1
    if t >= tree:
      break
  return vis

def check_visibility_for_tree_at(row, col):
  tree = forest[row][col]
  return \
    visible_for_direction("L", row, col, tree) or \
    visible_for_direction("R", row, col, tree) or \
    visible_for_direction("U", row, col, tree) or \
    visible_for_direction("D", row, col, tree)

def get_score_for_tree_at(row, col):
  tree = forest[row][col]
  return \
    score_for_direction("L", row, col, tree) * \
    score_for_direction("R", row, col, tree) * \
    score_for_direction("U", row, col, tree) * \
    score_for_direction("D", row, col, tree)

# Initialize forest, col_len, row_len
with open("input.txt", "r") as file:
  for row in file.readlines():
    row = [int(x) for x in row.strip()]
    if not col_len:
      col_len = len(row)
    forest.append(row)
  row_len = len(forest)

# Convenient way to iterate with "row" and "col" indexes
coord_generator = [(i // row_len, i % col_len) for i in range(row_len * col_len)]

visible = [check_visibility_for_tree_at(r, c) for r, c in coord_generator].count(True)
print("Part one:", visible)

max_score = max([get_score_for_tree_at(r, c) for r, c in coord_generator])
print("Part two:", max_score)
