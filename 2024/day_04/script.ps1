#!/opt/homebrew/bin/pwsh

$fileText = gc "./example.txt"

$rows = $fileText.Split('\n')
$flatForward = [string]::Join("Z", $rows)
$tmp = $flatForward.ToCharArray()
[Array]::Reverse($tmp)
$flatBackward = [string]::Join("", $tmp)
$colLen = $rows[0].Length
$sb = [System.Text.StringBuilder]::new()
0..$colLen | % {
  $i = $_
  $rows | % {
    $sb.Append($_[$i]) | Out-Null
  }
  $sb.Append("Z") | Out-Null
}
$rotatedRight = $sb.ToString()
$tmp = $rotatedRight.ToCharArray()
[Array]::Reverse($tmp)
$rotatedLeft = [String]::Join("", $tmp)

$total = 0
$total += [System.Text.RegularExpressions.Regex]::Count($flatForward, "XMAS")
$total += [System.Text.RegularExpressions.Regex]::Count($flatBackward, "XMAS")
$total += [System.Text.RegularExpressions.Regex]::Count($rotatedRight, "XMAS")
$total += [System.Text.RegularExpressions.Regex]::Count($rotatedLeft, "XMAS")
$total

#TODO gather all diagonal forms
