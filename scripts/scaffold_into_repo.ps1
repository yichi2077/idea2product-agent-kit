# Windows convenience wrapper. Canonical cross-platform installer is install.py.
param(
  [Parameter(Mandatory = $true)]
  [string]$TargetPath
)
$ErrorActionPreference = "Stop"
$args = @("scaffold", $TargetPath)
& python (Join-Path $PSScriptRoot "install.py") @args
