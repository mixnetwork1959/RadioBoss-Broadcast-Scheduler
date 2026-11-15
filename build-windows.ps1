# Build a separate portable test release without overwriting previous builds.
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$projectDirectory = $PSScriptRoot
$buildName = 'BroadcastScheduler-4.5.0-test'
$distDirectory = Join-Path $projectDirectory 'dist'
$exePath = Join-Path $distDirectory "$buildName.exe"

foreach ($required in @('scheduler.py', 'BroadcastScheduler.ico', 'tk_runtime_hook.py', 'templates')) {
    if (-not (Test-Path -LiteralPath (Join-Path $projectDirectory $required))) {
        throw "BUILD_INPUT_MISSING: $required"
    }
}

if (Test-Path -LiteralPath $exePath) {
    throw "BUILD_ALREADY_EXISTS: $exePath (move or rename it first; nothing was overwritten)"
}

Push-Location $projectDirectory
try {
    & py -m PyInstaller --version
    if ($LASTEXITCODE -ne 0) {
        throw 'PYINSTALLER_NOT_INSTALLED: run py -m pip install pyinstaller'
    }

    & py -m PyInstaller `
        --onefile `
        --windowed `
        --name $buildName `
        --distpath $distDirectory `
        --workpath (Join-Path $projectDirectory 'build\portable-test') `
        --specpath (Join-Path $projectDirectory 'build\specs') `
        --runtime-hook (Join-Path $projectDirectory 'tk_runtime_hook.py') `
        --icon (Join-Path $projectDirectory 'BroadcastScheduler.ico') `
        --add-data "$(Join-Path $projectDirectory 'BroadcastScheduler.ico');." `
        --add-data "$(Join-Path $projectDirectory 'templates');templates" `
        (Join-Path $projectDirectory 'scheduler.py')

    if ($LASTEXITCODE -ne 0) { throw "PYINSTALLER_BUILD_FAILED: $LASTEXITCODE" }

    if (-not (Test-Path -LiteralPath $exePath -PathType Leaf)) {
        throw "BUILD_OUTPUT_MISSING: $exePath"
    }
    Write-Host "BUILD_OK $exePath"
    Write-Host 'TEST: launch this EXE without settings.json; select the customer SDL.'
} finally {
    Pop-Location
}
