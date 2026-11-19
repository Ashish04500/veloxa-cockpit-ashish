param([switch]$Reingest, [switch]$InstallDependencies)


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
$DAY3 = Join-Path $RELEASE_ROOT "Day3_Wed_18Nov"
$DAY4 = Join-Path $RELEASE_ROOT "Day4_Thu_19Nov"

if (-not (Test-Path $DAY1)) {
    throw "Day 1 release folder missing: $DAY1"
}

if (-not (Test-Path $DAY2)) {
    throw "Day 2 release folder missing: $DAY2"
}

if (-not (Test-Path $DAY3)) {
    throw "Day 3 release folder missing: $DAY3"
}

if (-not (Test-Path $DAY4)) {
    throw "Day 4 release folder missing: $DAY4"
}

# 3. Ensure Python environment
$VENV_CREATED = $false

if (-not (Test-Path $VENV_PYTHON)) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
    & python -m venv (Join-Path $BACKEND "venv")
    if ($LASTEXITCODE -ne 0) { throw "Virtual environment creation failed." }
    $VENV_CREATED = $true
}

# 4. Install dependencies only when needed
if ($VENV_CREATED -or $InstallDependencies) {
    Write-Host "`nInstalling backend dependencies..." -ForegroundColor Yellow
    & $VENV_PYTHON -m pip install -r (Join-Path $BACKEND "requirements.txt")
    if ($LASTEXITCODE -ne 0) { throw "Backend dependency installation failed." }
} else {
    Write-Host "Using existing backend environment."
}

$NODE_MODULES = Join-Path $FRONTEND "node_modules"

if (-not (Test-Path $NODE_MODULES) -or $InstallDependencies) {
    Write-Host "`nInstalling frontend dependencies..." -ForegroundColor Yellow
    Push-Location $FRONTEND
    try {
        & npm.cmd install
        if ($LASTEXITCODE -ne 0) { throw "Frontend dependency installation failed." }
    }
    finally {
        Pop-Location
    }
} else {
    Write-Host "Using existing frontend dependencies."
}

# 5. Ingest only when processed data is missing or explicitly requested
$PROCESSED = Join-Path $ROOT "data\processed"
$NEEDS_INGEST = $false

foreach ($DAY in @("day1", "day2", "day3", "day4")) {
    if (-not (Test-Path (Join-Path $PROCESSED "${DAY}_documents.jsonl"))) {
        $NEEDS_INGEST = $true
    }
}

if ($Reingest -or $NEEDS_INGEST) {
    foreach ($DAY in @("day1", "day2", "day3", "day4")) {
        Write-Host "`nIngesting $DAY data..." -ForegroundColor Yellow
        & $VENV_PYTHON (Join-Path $BACKEND "app\ingest_${DAY}.py")
        if ($LASTEXITCODE -ne 0) { throw "$DAY ingestion failed." }
    }
} else {
    Write-Host "Processed data already exists. Skipping ingestion."
    Write-Host "Use .\run.ps1 -Reingest to refresh it."
}

# 6. Start services in the background, keeping this terminal available
$LOG_DIR = Join-Path $ROOT "logs"
New-Item -ItemType Directory -Force -Path $LOG_DIR | Out-Null

$BACKEND_OUT = Join-Path $LOG_DIR "backend-out.log"
$BACKEND_ERR = Join-Path $LOG_DIR "backend-error.log"
$FRONTEND_OUT = Join-Path $LOG_DIR "frontend-out.log"
$FRONTEND_ERR = Join-Path $LOG_DIR "frontend-error.log"

function Test-HttpEndpoint([string]$URL) {
    try {
        $null = Invoke-WebRequest -Uri $URL -UseBasicParsing -TimeoutSec 2
        return $true
    } catch {
        return $false
    }
}

function Wait-ForEndpoint([string]$URL, [int]$SECONDS = 20) {
    $deadline = (Get-Date).AddSeconds($SECONDS)
    do {
        if (Test-HttpEndpoint $URL) { return $true }
        Start-Sleep -Milliseconds 500
    } while ((Get-Date) -lt $deadline)
    return $false
}

$BACKEND_URL = "http://127.0.0.1:8000/"
$FRONTEND_URL = "http://127.0.0.1:5173/"

# Backend
$BACKEND_LISTENER = Get-NetTCPConnection -State Listen -LocalPort 8000 -ErrorAction SilentlyContinue |
    Select-Object -First 1

if ($BACKEND_LISTENER) {
    if (Test-HttpEndpoint $BACKEND_URL) {
        Write-Host "Reusing existing backend at $BACKEND_URL" -ForegroundColor Green
    } else {
        throw "Port 8000 is occupied, but the backend health endpoint did not respond."
    }
} else {
    Write-Host "`nStarting backend..." -ForegroundColor Green
    Start-Process -FilePath $VENV_PYTHON `
        -WorkingDirectory $ROOT `
        -ArgumentList @(
            "-m", "uvicorn", "app.main:app",
            "--app-dir", $BACKEND,
            "--host", "127.0.0.1",
            "--port", "8000",
            "--reload"
        ) `
        -RedirectStandardOutput $BACKEND_OUT `
        -RedirectStandardError $BACKEND_ERR `
        -WindowStyle Hidden | Out-Null

    if (-not (Wait-ForEndpoint $BACKEND_URL)) {
        Write-Host "Backend failed to become ready. Check logs/backend-error.log" -ForegroundColor Red
        throw "Backend startup timed out."
    }
}

# Frontend
$FRONTEND_LISTENER = Get-NetTCPConnection -State Listen -LocalPort 5173 -ErrorAction SilentlyContinue |
    Select-Object -First 1

if ($FRONTEND_LISTENER) {
    if (Test-HttpEndpoint $FRONTEND_URL) {
        Write-Host "Reusing existing frontend at $FRONTEND_URL" -ForegroundColor Green
    } else {
        throw "Port 5173 is occupied, but the frontend did not respond."
    }
} else {
    Write-Host "Starting frontend..." -ForegroundColor Green
    Start-Process -FilePath $env:ComSpec `
        -WorkingDirectory $FRONTEND `
        -ArgumentList '/c "npm.cmd run dev -- --host 127.0.0.1 --port 5173 --strictPort"' `
        -RedirectStandardOutput $FRONTEND_OUT `
        -RedirectStandardError $FRONTEND_ERR `
        -WindowStyle Hidden | Out-Null

    if (-not (Wait-ForEndpoint $FRONTEND_URL)) {
        Write-Host "Frontend failed to become ready. Check logs/frontend-error.log" -ForegroundColor Red
        throw "Frontend startup timed out."
    }
}

Write-Host "`n======================================" -ForegroundColor Green
Write-Host " VELOXA CEO COCKPIT IS READY" -ForegroundColor Green
Write-Host " Frontend: $FRONTEND_URL" -ForegroundColor Green
Write-Host " Backend:  $BACKEND_URL" -ForegroundColor Green
Write-Host " API Docs: http://127.0.0.1:8000/docs" -ForegroundColor Green
Write-Host " Logs:     $LOG_DIR" -ForegroundColor Green
Write-Host "======================================`n" -ForegroundColor Green
