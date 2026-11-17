
$ErrorActionPreference = "Stop"

$ROOT = $PSScriptRoot
$BACKEND = Join-Path $ROOT "backend"
$FRONTEND = Join-Path $ROOT "frontend"
$VENV_PYTHON = Join-Path $BACKEND "venv\Scripts\python.exe"
$RELEASE_ROOT = Join-Path $ROOT "data\raw\Veloxa_Hackathon_Release_Packs"

Write-Host "`n======================================" -ForegroundColor Cyan
Write-Host " VELOXA CEO COCKPIT - STARTUP" -ForegroundColor Cyan
Write-Host "======================================`n" -ForegroundColor Cyan

# 1. Check prerequisites
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python is not installed or not available in PATH."
}

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    throw "Node.js is not installed or not available in PATH."
}

if (-not (Get-Command npm.cmd -ErrorAction SilentlyContinue)) {
    throw "npm.cmd was not found. Install Node.js with npm."
}

# 2. Check release data
$DAY1 = Join-Path $RELEASE_ROOT "Day1_Mon_16Nov"
$DAY2 = Join-Path $RELEASE_ROOT "Day2_Tue_17Nov"

if (-not (Test-Path $DAY1)) {
    throw "Day 1 release folder missing: $DAY1"
}

if (-not (Test-Path $DAY2)) {
    throw "Day 2 release folder missing: $DAY2"
}

# 3. Create Python virtual environment if needed
if (-not (Test-Path $VENV_PYTHON)) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv (Join-Path $BACKEND "venv")
}

# 4. Install backend dependencies
Write-Host "`nInstalling backend dependencies..." -ForegroundColor Yellow
& $VENV_PYTHON -m pip install -r (Join-Path $BACKEND "requirements.txt")

if ($LASTEXITCODE -ne 0) {
    throw "Backend dependency installation failed."
}

# 5. Install frontend dependencies
Write-Host "`nInstalling frontend dependencies..." -ForegroundColor Yellow
Push-Location $FRONTEND

try {
    & npm.cmd install

    if ($LASTEXITCODE -ne 0) {
        throw "Frontend dependency installation failed."
    }
}
finally {
    Pop-Location
}

# 6. Ingest Day 1 and Day 2 source files
Write-Host "`nIngesting Day 1 data..." -ForegroundColor Yellow
& $VENV_PYTHON (Join-Path $BACKEND "app\ingest_day1.py")

if ($LASTEXITCODE -ne 0) {
    throw "Day 1 ingestion failed."
}

Write-Host "`nIngesting Day 2 data..." -ForegroundColor Yellow
& $VENV_PYTHON (Join-Path $BACKEND "app\ingest_day2.py")

if ($LASTEXITCODE -ne 0) {
    throw "Day 2 ingestion failed."
}

# 7. Launch backend in a separate PowerShell window
Write-Host "`nStarting backend..." -ForegroundColor Green

$BACKEND_COMMAND = "Set-Location '$ROOT'; & '$VENV_PYTHON' -m uvicorn app.main:app --app-dir backend --reload"

Start-Process powershell.exe -ArgumentList @(
    "-NoExit",
    "-Command",
    $BACKEND_COMMAND
)

# 8. Launch frontend in a separate PowerShell window
Write-Host "Starting frontend..." -ForegroundColor Green

$NPM = (Get-Command npm.cmd).Source
$FRONTEND_COMMAND = "Set-Location '$FRONTEND'; & '$NPM' run dev"

Start-Process powershell.exe -ArgumentList @(
    "-NoExit",
    "-Command",
    $FRONTEND_COMMAND
)

Write-Host "`n======================================" -ForegroundColor Green
Write-Host " Startup commands launched." -ForegroundColor Green
Write-Host " Frontend: http://localhost:5173" -ForegroundColor Green
Write-Host " Backend:  http://127.0.0.1:8000" -ForegroundColor Green
Write-Host " API Docs: http://127.0.0.1:8000/docs" -ForegroundColor Green
Write-Host "======================================`n" -ForegroundColor Green
