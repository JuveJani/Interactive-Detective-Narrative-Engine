# Complete diagnostic run with all reports
param(
    [Parameter(Mandatory = $true)][string]$Package,
    [int]$Seed = 42,
    [int]$Runs = 1000,
    [int]$MaxStates = 200000
)
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
& .\.venv\Scripts\Activate.ps1
python -m idne.sim_v2 diagnose $Package --seed $Seed --runs $Runs --max-states $MaxStates
