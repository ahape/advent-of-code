#!/opt/homebrew/bin/pwsh 

#$raw_input = gc "example.txt"
$raw_input = gc "input.txt"

$chars = $raw_input.ToCharArray()

$sb = $mul_params = ""
$mul_started = $false
$total = 0

function Reset-Vars {
  $global:mul_started = $false
  $global:mul_params = ""
}

$chars | % {
  $sb += $_
  if ($sb.EndsWith("mul(")) {
    $mul_started = $true
    $mul_params = ""
  } elseif ($mul_started -and $_ -eq ")") {
    ($a, $b) = $mul_params.Split(',')
    $a2 = $b2 = $null
    if ([int]::TryParse($a, [ref]$a2) -and
        [int]::TryParse($b, [ref]$b2)) {
      $total += ($a2 * $b2)
    }
    Reset-Vars
  } elseif ($mul_started) {
    $n = $null
    if ([int]::TryParse($_, [ref]$n)) {
      $mul_params += $n
    } elseif ($_ -eq "," -and $mul_params -notcontains ",") {
      $mul_params += ","
    } else {
      Reset-Vars
    }
  } else {
    Reset-Vars
  }
}

Write-Host $total
