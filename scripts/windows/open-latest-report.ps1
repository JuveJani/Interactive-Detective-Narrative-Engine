# Open the latest Simulator v2 report folder in Explorer
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
$base = Join-Path $Root "simulation_output_v2"
if (-not (Test-Path $base)) {
    Write-Host "No reports yet at $base"
    exit 1
}
$latest = Get-ChildItem $base -Directory | Sort-Object Name -Descending | Select-Object -First 1
Write-Host "Latest report: $($latest.FullName)"
Start-Process explorer.exe $latest.FullName
