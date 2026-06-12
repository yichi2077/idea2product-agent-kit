# Windows convenience wrapper. Canonical cross-platform installer is install.py.
param(
  [ValidateSet("both", "codex", "claude-code")]
  [string]$Target = "both"
)
$ErrorActionPreference = "Stop"
& python (Join-Path $PSScriptRoot "install.py") skills --target $Target
