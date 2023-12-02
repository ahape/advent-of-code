import re

num_extractor_rx = re.compile(r"(\d|one|two|three|four|five|six|seven|eight|nine)")
num_map = {
  "one": 1,
  "two": 2,
  "three": 3,
  "four": 4,
  "five": 5,
  "six": 6,
  "seven": 7,
  "eight": 8,
  "nine": 9,
}

def solve(data):
  total = 0
  for row in data:
    num = extract_two_digit_num(row)
    total += num
  return total

def extract_two_digit_num(row):
  digits = []
  for m in num_extractor_rx.finditer(row):
    num = m[0]
    if num.isdigit():
      digits.append(num)
    else:
      digits.append(num_map[num])
  res = f"{digits[0]}{digits[-1]}"
  print(row, "-->", int(res))
  return int(res)

def main():
  data = []
  #with open("example-1.txt") as f:
  #with open("example-2.txt") as f:
  with open("example-3.txt") as f:
  #with open("input.txt") as f:
    for row in f.readlines():
      row = row.strip()
      if row:
        data.append(row)

  answer = solve(data)
  print(answer)

if __name__ == "__main__":
  main()
