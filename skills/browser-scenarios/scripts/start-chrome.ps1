# Start the scenario Chrome: its own profile, debugging port 9223 (or $env:SCENARIO_CDP_PORT) on this machine only. Leave it open.
# Windows PowerShell. Usage: .\start-chrome.ps1 [url]
param(
    [string]$Url = "about:blank"
)

$ProfileDir = "$env:USERPROFILE\.gemini\browser-profile"
$CdpPort = if ($env:SCENARIO_CDP_PORT) { $env:SCENARIO_CDP_PORT } else { "9223" }
$ChromeCandidates = @(
    $env:CHROME_BIN,
    "C:\Program Files\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
    "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
) | Where-Object { $_ -and (Test-Path $_) }
$ChromeExe = if ($ChromeCandidates.Count -gt 0) { $ChromeCandidates[0] } else { "C:\Program Files\Google\Chrome\Application\chrome.exe" }

if (-not (Test-Path $ProfileDir)) {
    New-Item -ItemType Directory -Path $ProfileDir -Force | Out-Null
}

function Test-ChromePort {
    try {
        $res = Invoke-RestMethod -Uri "http://127.0.0.1:$CdpPort/json/version" -TimeoutSec 2 -ErrorAction Stop
        return ($null -ne $res)
    } catch {
        return $false
    }
}

if (Test-ChromePort) {
    Write-Host "Something already answers on port $CdpPort; assuming it is the scenario Chrome."
    exit 0
}

if (-not (Test-Path $ChromeExe)) {
    Write-Error "Chrome not found at $ChromeExe"
    exit 1
}

Start-Process -FilePath $ChromeExe -ArgumentList @(
    "--remote-debugging-port=$CdpPort",
    "--user-data-dir=$ProfileDir",
    "--no-first-run",
    "--no-default-browser-check",
    $Url
)

for ($i = 0; $i -lt 15; $i++) {
    if (Test-ChromePort) {
        Write-Host "Scenario Chrome is up. Open a build with browser-login."
        exit 0
    }
    Start-Sleep -Seconds 1
}

Write-Error "Chrome did not open the debugging port. If this profile is already open in a Chrome started without the port, close that window and run again."
exit 1
