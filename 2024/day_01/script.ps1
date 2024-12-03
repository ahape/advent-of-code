#!/opt/homebrew/bin/pwsh
#
# Setup
#
$col_1_const, $col_2_const = @(), @()
(gc ./input.txt) -split "\n" | % {
  $x = $_ -split "\s+"
  $col_1_const+=$x[0]
  $col_2_const+=$x[1]
}
#
# Part One
#
$c1, $c2 = ($col_1_const|Sort), ($col_2_const|Sort)
0..$c1.Count | % `
  -Begin { $sum = 0 } `
  -Process {
    $a, $b = $c1[$_], $c2[$_]
    $sum += [math]::Max($a, $b) - [math]::Min($a, $b)
  } `
  -End { "Part One: $sum" }
#
# Part Two
#
$c1, $c2 = ($col_1_const|Sort|gu), ($col_2_const|Sort)
$c1 | % `
  -Begin { $sum = 0 } `
  -Process {
    $o = $_
    $sum += ($c2 | ? { $_ -eq $o }).Count * $o
  } `
  -End { "Part Two: $sum" }
