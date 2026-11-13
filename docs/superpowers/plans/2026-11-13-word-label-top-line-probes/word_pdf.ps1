param([string]$Path, [string]$Pdf)
# Word's own render of a copy to PDF, read-only, never saving the document;
# stops only its own Word process.
$before = @(Get-Process WINWORD -ErrorAction SilentlyContinue | ForEach-Object { $_.Id })
$word = New-Object -ComObject Word.Application
$mine = @(Get-Process WINWORD | Where-Object { $before -notcontains $_.Id })
if ($mine.Count -ne 1) { $word.Quit(); throw "could not identify this script's own Word process" }
$wpid = $mine[0].Id
try {
  $word.Visible = $false
  $doc = $word.Documents.Open([ref]$Path, [ref]$false, [ref]$true)
  $doc.ExportAsFixedFormat($Pdf, 17)
  $doc.Close([ref]$false)
  "wrote $Pdf"
} finally {
  $word.Quit([ref]$false)
  Start-Sleep -Milliseconds 1500
  if (Get-Process -Id $wpid -ErrorAction SilentlyContinue) { Stop-Process -Id $wpid }
}
