# User-run shorthand for browser-login: mod-login <build> [product]
# Never run by the AI.
param(
    [Parameter(Position=0, Mandatory=$true)]
    [string]$Build,
    [Parameter(Position=1)]
    [string]$Product
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RunScript = Join-Path $ScriptDir "run.ps1"
if ($Product) {
    & $RunScript $Build $Product
} else {
    & $RunScript $Build
}
exit $LASTEXITCODE
