param([string]$Root)
# For every lab folder under $Root holding A.docx and D2.docx, Word renders
# each to PDF (read-only, never saving; one Word instance, stopped by its
# own process id at the end).
$before = @(Get-Process WINWORD -ErrorAction SilentlyContinue | ForEach-Object { $_.Id })
$word = New-Object -ComObject Word.Application
$mine = @(Get-Process WINWORD | Where-Object { $before -notcontains $_.Id })
if ($mine.Count -ne 1) { $word.Quit(); throw "could not identify this script's own Word process" }
$wpid = $mine[0].Id
try {
  $word.Visible = $false
  foreach ($dir in Get-ChildItem -Directory $Root) {
    foreach ($name in "A", "D2") {
      $doc = $word.Documents.Open([ref]"$($dir.FullName)\$name.docx", [ref]$false, [ref]$true)
      $doc.ExportAsFixedFormat("$($dir.FullName)\$name.pdf", 17)
      $doc.Close([ref]$false)
    }
    "rendered $($dir.Name)"
  }
} finally {
  $word.Quit([ref]$false)
  Start-Sleep -Milliseconds 1500
  if (Get-Process -Id $wpid -ErrorAction SilentlyContinue) { Stop-Process -Id $wpid }
}
