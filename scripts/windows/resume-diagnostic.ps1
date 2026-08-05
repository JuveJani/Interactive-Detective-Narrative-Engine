# Resume interrupted diagnostic (uses checkpoint in output folder)
param(
    [Parameter(Mandatory = $true)][string]$Package,
    [string]$OutputBase = "simulation_output_v2"
)
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
& .\.venv\Scripts\Activate.ps1
# To cancel a running diagnostic, create .cancel in the output folder or press Ctrl+C
python -m idne.sim_v2 diagnose $Package --output-base $OutputBase --resume
