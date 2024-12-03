#!/opt/homebrew/bin/pwsh
#
# Setup
#
$c1, $c2 = @(), @()
(gc ./input.txt) -split "\n" | % {
  $x = $_ -split "\s+"
  $c1+=$x[0]
  $c2+=$x[1]
}
$c1, $c2 = ($c1|Sort), ($c2|Sort)
#
# Part One
#
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
$c1 | gu | % `
  -Begin { $sum = 0 } `
  -Process {
    $o = $_
    $sum += ($c2 | ? { $_ -eq $o }).Count * $o
  } `
  -End { "Part Two: $sum" }
