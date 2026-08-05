# Export offline AI context for a finding from a prior run
param(
    [Parameter(Mandatory = $true)][string]$OutputFolder,
    [Parameter(Mandatory = $true)][string]$FindingId
)
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
& .\.venv\Scripts\Activate.ps1
python -m idne.sim_v2 export-ai-context $OutputFolder --finding $FindingId
