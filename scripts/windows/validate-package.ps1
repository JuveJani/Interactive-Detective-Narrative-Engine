# Validate a canonical .idne or unpacked package
param(
    [Parameter(Mandatory = $true)][string]$Package
)
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
& .\.venv\Scripts\Activate.ps1
python -m idne.sim_v2 validate $Package
