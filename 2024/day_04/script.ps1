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

  $numCols = $matrix[0].Length
  $sb = [System.Text.StringBuilder]::new()
  0..$numCols | % {
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

  $numRows = $matrix.Length
  $numCols = $matrix[0].Length
  $sb = [System.Text.StringBuilder]::new()
  $i = 0
  0..($numRows + $numCols) | % {
    $d = $_
    0..($d + 1) | % {
      $col = $_
      $row = $d - $col
      if ($row -lt $numRows -and $col -lt $numCols) {
        $sb.Append($matrix[$row][$col]) | Out-Null
        $i++
        if ($i % $numCols -eq 0) {
          $sb.Append("\n") | Out-Null
        }
      }
    }
  }
  return "$sb"
}

$lines = $fileText.Split('\n')
$flatForward = $lines -join $DELIM
$flatBackward = Reverse-String $flatForward
$rotatedRight = Rotate-RightFlat $lines
$rotatedLeft = Reverse-String $rotatedRight
$flatDiagonal = Flatten-Diagonals $lines

$lines
"======"
$flatDiagonal.Split('\n')
#[System.Linq.Enumerable]::Chunk($flatDiagonal, $lines[0].Length) -join '\n'
<#
$all = @($flatForward, $flatBackward, $rotatedRight, $rotatedLeft, $flatDiagonal) -join "Z"
$total = [System.Text.RegularExpressions.Regex]::Count($all, $searchTerm)
Write-Host $total
#>
