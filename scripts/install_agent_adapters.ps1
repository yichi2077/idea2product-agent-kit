# Windows convenience wrapper. Canonical cross-platform installer is install.py.
param(
  [Parameter(Mandatory = $true)]
  [string]$TargetPath,

  [ValidateSet("all", "codex", "cursor", "claude-code", "opencode", "hermes", "openclaw", "generic")]
  [string]$Agent = "all",

  [switch]$InstallUserSkills
)
$ErrorActionPreference = "Stop"
$args = @("adapters", $TargetPath, "--agent", $Agent)
if ($InstallUserSkills) { $args += "--install-user-skills" }
& python (Join-Path $PSScriptRoot "install.py") @args
