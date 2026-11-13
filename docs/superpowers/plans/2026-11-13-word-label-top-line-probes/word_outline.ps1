param([string]$Path)
# Read-only: Word's own outline level and in-table flag for each paragraph
# that has an outline level. Never saves; quits only its own instance.
$before = @(Get-Process WINWORD -ErrorAction SilentlyContinue | ForEach-Object { $_.Id })
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$mine = @(Get-Process WINWORD | Where-Object { $before -notcontains $_.Id })
if ($mine.Count -ne 1) { throw "could not identify this script's own Word process" }
$wpid = $mine[0].Id
try {
  $missing = [Type]::Missing
  $doc = $word.Documents.Open([ref]$Path, [ref]$false, [ref]$true)
  $i = 0
  foreach ($p in $doc.Paragraphs) {
    $i++
    $lvl = $p.OutlineLevel
    if ($lvl -lt 10) {
      $inTable = $p.Range.Information(12)
      $text = $p.Range.Text.Trim()
      if ($text.Length -gt 40) { $text = $text.Substring(0, 40) }
      "{0,4} lvl={1} table={2} style={3} | {4}" -f $i, $lvl, $inTable, $p.Style.NameLocal, $text
    }
  }
  $doc.Close([ref]$false)
} finally {
  $word.Quit([ref]$false)
  Start-Sleep -Milliseconds 500
  if (Get-Process -Id $wpid -ErrorAction SilentlyContinue) { Stop-Process -Id $wpid }
}
