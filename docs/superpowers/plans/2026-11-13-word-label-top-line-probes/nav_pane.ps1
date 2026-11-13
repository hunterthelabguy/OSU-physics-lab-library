param([string]$Path)
# Opens a copy read-only in a visible Word, shows the Navigation pane,
# expands every heading in it (critique variant: focus each entry and
# press Right, only while this Word is in front), and lists the pane's
# heading entries in order. Never saves; stops only its own Word process.
Add-Type -AssemblyName UIAutomationClient, UIAutomationTypes
$A = [System.Windows.Automation.AutomationElement]
$before = @(Get-Process WINWORD -ErrorAction SilentlyContinue | ForEach-Object { $_.Id })
$word = New-Object -ComObject Word.Application
$mine = @(Get-Process WINWORD | Where-Object { $before -notcontains $_.Id })
if ($mine.Count -ne 1) { $word.Quit(); throw "could not identify this script's own Word process" }
$wpid = $mine[0].Id
function Tabs {
  $cond = New-Object System.Windows.Automation.PropertyCondition($A::ProcessIdProperty, $wpid)
  $cls = New-Object System.Windows.Automation.PropertyCondition($A::ClassNameProperty, "NetUINavPaneTab")
  $out = @()
  foreach ($w in $A::RootElement.FindAll([System.Windows.Automation.TreeScope]::Children, $cond)) {
    $out += @($w.FindAll([System.Windows.Automation.TreeScope]::Descendants, $cls))
  }
  return $out
}
try {
  $word.Visible = $true
  $doc = $word.Documents.Open([ref]$Path, [ref]$false, [ref]$true)
  $doc.ActiveWindow.DocumentMap = $true
  Start-Sleep -Seconds 4
  # Focus each entry in the pane and press Right, only while this Word is in front.
  Add-Type -AssemblyName System.Windows.Forms
  Add-Type -Namespace W -Name U -MemberDefinition '[DllImport("user32.dll")] public static extern System.IntPtr GetForegroundWindow(); [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(System.IntPtr h, out uint p);'
  $round = 0
  do {
    $n0 = @(Tabs).Count
    foreach ($t in @(Tabs)) {
      $t.SetFocus(); Start-Sleep -Milliseconds 150
      [uint32]$fp = 0; [void][W.U]::GetWindowThreadProcessId([W.U]::GetForegroundWindow(), [ref]$fp)
      if ($fp -ne $wpid) { "NOT SENT: foreground window belongs to process $fp"; break }
      [System.Windows.Forms.SendKeys]::SendWait("{RIGHT}"); Start-Sleep -Milliseconds 250
    }
    $round++
  } while (@(Tabs).Count -gt $n0 -and $round -lt 6)
  $all = @(Tabs)
  foreach ($t in $all) { $t.Current.Name }
  "PANE ENTRIES: $($all.Count) after $round expand rounds"
  $doc.Close([ref]$false)
} finally {
  $word.Quit([ref]$false)
  Start-Sleep -Milliseconds 1500
  if (Get-Process -Id $wpid -ErrorAction SilentlyContinue) { Stop-Process -Id $wpid }
}
