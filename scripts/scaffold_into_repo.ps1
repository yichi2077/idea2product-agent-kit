# Windows convenience wrapper. Canonical cross-platform installer is install.py.
param(
  [Parameter(Mandatory = $true)]
  [string]$TargetPath,
  [switch]$Verify
)
$ErrorActionPreference = "Stop"
$args = @("scaffold", $TargetPath)
if ($Verify) { $args += "--verify" }
& python (Join-Path $PSScriptRoot "install.py") @args
