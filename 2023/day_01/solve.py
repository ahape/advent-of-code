num_map = {
  "one": "1",
  "two": "2",
  "three": "3",
  "four": "4",
  "five": "5",
  "six": "6",
  "seven": "7",
  "eight": "8",
  "nine": "9",
}

def solve(data):
  return sum(extract_two_digit_num(row) for row in data)

def extract_two_digit_num(row):
  first_num = last_num = first_index = last_index = None
  for word, digit in num_map.items():
    for num in [word, digit]:
      if num in row:
        s, e = row.index(num), row.rindex(num)
        if first_index is None or s < first_index:
          first_index = s
          first_num = num if num.isdigit() else num_map[num] 
        if last_index is None or e > last_index:
          last_index = e
          last_num = num if num.isdigit() else num_map[num] 
  res = first_num + last_num
  #print(row, "-->", res)
  return int(res)

def read_data(file):
  with open(file) as f:
    text = f.read().strip()
    return text.split("\n")

def main():
  #data = read_data("example-1.txt")
  #data = read_data("example-2.txt")
  #data = read_data("example-3.txt")
  data = read_data("input.txt")
  answer = solve(data)
  print("The Answer:", answer)

if __name__ == "__main__":
  main()
