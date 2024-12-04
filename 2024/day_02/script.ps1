#!/opt/homebrew/bin/pwsh
#
# Setup
#
function distance {
  param([int]$a, [int]$b)
  $max = [math]::Max($a, $b)
  $min = [math]::Min($a, $b)
  return $max - $min
}
function iterLevels {
  param([int[]]$levels)
  $ret = 0
  0..($levels.Count - 1) | % `
    -Begin {
      $dead = $false
      $prev = $asc = $null
    } `
    -Process {
      $cur = [int]$levels[$_]
      if ($prev -ne $null -and -not $dead) {
        $i_asc = $prev -lt $cur
        if ($asc -eq $null) { $asc = $i_asc }
        if ($i_asc -ne $asc) { $dead = $true }
        if ($prev -eq $cur) { $dead = $true }
        if (-not $dead) {
          $dead = (distance $prev $cur) -gt 3
        }
      }
      $prev = $cur
    } `
    -End {
      if (-not $dead) {
        $ret = 1
      }
    }
  return $ret
}
$reports = (gc ./input.txt) -split "`n"
#
# Part One
#
$safe = 0
0..($reports.Count - 1) | % {
  $levels = $reports[$_] -split "\s+" | % { [int]$_ }
  $safe += (iterLevels $levels)
}
"Safe count is $safe"
#
# Part Two
#
$safe = 0
0..($reports.Count - 1) | % {
  $levels = $reports[$_] -split "\s+" | % { [int]$_ }
  if ((iterLevels $levels) -eq 1) {
    $safe += 1
  } else {
    $levelsLastIndex = $levels.Count - 1
    $safeBuilder = 0
    0..$levelsLastIndex | % {
      $missing1 = @()
      $missing1 += $levels | select -First $_ # wrong/ TODO
      $missing1 += $levels | select -Skip $_
      $safeBuilder += (iterLevels $missing1)
    }
    if ($safeBuilder -ge $levelsLastIndex) {
      $safe += 1
    }
  }
}
"Safe count is $safe"
