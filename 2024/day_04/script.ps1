#!/opt/homebrew/bin/pwsh

$DELIM = "Z"
$searchTerm = "XMAS"
$fileText = gc "./example.txt"

function Reverse-String {
  param([string]$str)

  $charArray = $str.ToCharArray()
  [Array]::Reverse($charArray)
  return -join $charArray
}

function Rotate-RightFlat {
  param([string[]]$matrix)

  $colLen = $matrix[0].Length
  $sb = [System.Text.StringBuilder]::new()
  0..$colLen | % {
    $i = $_
    $matrix | % {
      $sb.Append($_[$i]) | Out-Null
    }
    $sb.Append($DELIM) | Out-Null
  }
  return $sb.ToString()
}

function Flatten-Diagonals {
  param([string[]]$matrix)

  <#

matrix = [
  ["A", "B", "C"],
  ["E", "F", "G"],
  ["H", "I", "J"],
]
num_rows = len(matrix)
num_cols = len(matrix[0])
s = ""
for d in range(0, num_rows + num_cols):
  for col in range(0, d + 1):
    row = d - col
    if row < num_rows and col < num_cols:
      s += matrix[row][col]

print(s) # AEBHFCIGJ

  #>
}

$lines = $fileText.Split('\n')
$flatForward = $lines -join $DELIM
$flatBackward = Reverse-String $flatForward
$rotatedRight = Rotate-RightFlat $lines
$rotatedLeft = Reverse-String $rotatedRight

$all = @($flatForward, $flatBackward, $rotatedRight, $rotatedLeft) -join "Z"
$total = [System.Text.RegularExpressions.Regex]::Count($all, $searchTerm)
Write-Host $total

