# IDNE Simulator v2 — Windows installation (no admin required)
# Run from repository root in PowerShell 5.1+

$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location $Root

Write-Host "IDNE Simulator v2 — install"
Write-Host "Repository: $(Get-Location)"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        $py = "py -3"
    } else {
        throw "Python 3 not found. Install Python 3.11+ from python.org (user install, no admin)."
    }
} else {
    $py = "python"
}

& $py -m venv .venv
& .\.venv\Scripts\Activate.ps1
& python -m pip install --upgrade pip
if (Test-Path "requirements.txt") {
    & python -m pip install -r requirements.txt
}

Write-Host ""
Write-Host "Done. Activate with: .\.venv\Scripts\Activate.ps1"
Write-Host "Validate: python -m idne.sim_v2 validate tests\fixtures\sim_v2_solo"
