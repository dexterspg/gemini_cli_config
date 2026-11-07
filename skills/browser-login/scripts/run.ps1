# Starts the scenario Chrome if needed, then opens the product, signing in first when the build allows.
# Windows PowerShell. Usage: .\run.ps1 <build> [product]
param(
    [Parameter(Position=0, Mandatory=$true)]
    [string]$Build,
    [Parameter(Position=1)]
    [string]$Product
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $env:SCENARIO_CDP_PORT) { $env:SCENARIO_CDP_PORT = "9223" }

function Test-ChromePort {
    try {
        $res = Invoke-RestMethod -Uri "http://127.0.0.1:$($env:SCENARIO_CDP_PORT)/json/version" -TimeoutSec 2 -ErrorAction Stop
        return ($null -ne $res)
    } catch {
        return $false
    }
}

if (-not (Test-ChromePort)) {
    $startScript = Join-Path (Split-Path (Split-Path $ScriptDir -Parent) -Parent) "browser-scenarios\scripts\start-chrome.ps1"
    if (Test-Path $startScript) {
        & "$startScript" | Out-Null
    }
}

$loginPy = Join-Path $ScriptDir "login.py"
if ($Product) {
    python "$loginPy" $Build $Product
} else {
    python "$loginPy" $Build
}
exit $LASTEXITCODE
