# Activate virtual environment (no admin)
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
& .\.venv\Scripts\Activate.ps1
Write-Host "Virtual environment active: $(Get-Location)"
