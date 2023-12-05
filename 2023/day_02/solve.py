def read_data(file):
  with open(file) as f:
    text = f.read().strip()
    return text.split("\n")

def get_game_actions(row):
  act_map = { "red": [], "green": [], "blue": [] }
  for sequence in row.strip().split(";"):
    seen = set()
    for action in sequence.strip().split(","):
      [num, color] = action.strip().split(" ")
      if color in seen:
        # Acct for mult pulls for a single color in a round
        act_map[color][-1] += int(num)
      else:
        act_map[color].append(int(num))
      seen.add(color)
  return act_map

def part_1(data, thresholds):
  possible_games = []
  for i, row in enumerate(data):
    actions = get_game_actions(row.split(": ")[1]) # [game, actions]
    if max(actions["red"]) <= thresholds[0] and \
       max(actions["green"]) <= thresholds[1] and \
       max(actions["blue"]) <= thresholds[2]:
      possible_games.append(i + 1)
  return sum(possible_games)

def part_2(data):
  powers = []
  for i, row in enumerate(data):
    actions = get_game_actions(row.split(": ")[1]) # [game, actions]
    powers.append(max(actions["red"]) * max(actions["green"]) * max(actions["blue"]))
  return sum(powers)

def main():
  #data = read_data("example-1.txt")
  data = read_data("input.txt")
  #answer = part_1(data, (12,13,14))
  answer = part_2(data)
  print("The Answer:", answer)

if __name__ == "__main__":
  main()
