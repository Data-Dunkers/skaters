# ==============================================================================
# DATA DUNKERS - AUTOMATED POCKETBASE & LAN SERVER SETUP
# ==============================================================================

# Ensure script is running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Error "Please re-run this script as Administrator (Right-click PowerShell -> Run as Administrator)."
    exit
}

# ------------------------------------------------------------------------------
# STEP 1: Check WSL Installation
# ------------------------------------------------------------------------------
Write-Host "`n[1/4] Checking WSL 2 installation status..." -ForegroundColor Cyan
$wslStatus = wsl --status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "WSL is not installed on this system." -ForegroundColor Yellow
    Write-Host "Installing WSL now... A system restart will be required." -ForegroundColor Yellow
    wsl --install
    Write-Host "`n=================================================================" -ForegroundColor Red
    Write-Host "ACTION REQUIRED: Please REBOOT your computer now." -ForegroundColor Red
    Write-Host "After rebooting, re-run this PowerShell script as Administrator." -ForegroundColor Red
    Write-Host "=================================================================`n" -ForegroundColor Red
    exit
}
Write-Host "WSL is installed and ready." -ForegroundColor Green

# ------------------------------------------------------------------------------
# STEP 2: Configure Windows Firewall and Network Profile
# ------------------------------------------------------------------------------
Write-Host "`n[2/4] Configuring Firewall and Network Profile..." -ForegroundColor Cyan

# Set active network profiles to Private
Get-NetConnectionProfile | Where-Object NetworkCategory -eq 'Public' | Set-NetConnectionProfile -NetworkCategory Private
Write-Host "Active network profiles set to Private." -ForegroundColor Green

# Add Firewall Rule for Port 80
$fwRule = Get-NetFirewallRule -DisplayName "PocketBase LAN Port 80" -ErrorAction SilentlyContinue
if (-not $fwRule) {
    New-NetFirewallRule -DisplayName "PocketBase LAN Port 80" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 80 | Out-Null
    Write-Host "Inbound Firewall rule created for TCP Port 80." -ForegroundColor Green
} else {
    Write-Host "Firewall rule for TCP Port 80 already exists." -ForegroundColor Green
}

# ------------------------------------------------------------------------------
# STEP 3: Setup Project Directory Structure & Download Files from GitHub
# ------------------------------------------------------------------------------
Write-Host "`n[3/4] Setting up project folder structure..." -ForegroundColor Cyan
$projectDir = "C:\my-lan-app"
New-Item -ItemType Directory -Force -Path "$projectDir\pb_data" | Out-Null
New-Item -ItemType Directory -Force -Path "$projectDir\pb_public" | Out-Null
Set-Location -Path $projectDir

Write-Host "Fetching setup files from GitHub..." -ForegroundColor Cyan
$zipPath = "$env:TEMP\skaters_repo.zip"
$extractPath = "$env:TEMP\skaters_repo_extracted"

# Clean up previous downloads if existing
if (Test-Path $zipPath) { Remove-Item -Force $zipPath }
if (Test-Path $extractPath) { Remove-Item -Force -Recurse $extractPath }

Invoke-WebRequest -Uri "https://github.com/Data-Dunkers/skaters/archive/refs/heads/main.zip" -OutFile $zipPath
Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force
$repoRoot = "$extractPath\skaters-main"

# Copy Dockerfile, docker-compose.yaml and pb_migrations from /setup
$setupPath = "$repoRoot\setup"
if (Test-Path $setupPath) {
    Copy-Item -Path "$setupPath\Dockerfile" -Destination "$projectDir\Dockerfile" -Force
    Copy-Item -Path "$setupPath\docker-compose.yaml" -Destination "$projectDir\docker-compose.yml" -Force
    Copy-Item -Path "$setupPath\pb_migrations" -Destination "$projectDir\pb_migrations" -Recurse -Force
    Write-Host "Downloaded Dockerfile, docker-compose.yml and pb_migrations from GitHub." -ForegroundColor Green
} else {
    Write-Warning "Failed to locate setup directory in downloaded repository."
}

# Copy files from /docs to pb_public
$docsPath = "$repoRoot\docs"
if (Test-Path $docsPath) {
    Copy-Item -Path "$docsPath\*" -Destination "$projectDir\pb_public" -Recurse -Force
    Write-Host "Successfully downloaded and extracted static files to pb_public." -ForegroundColor Green
} else {
    Write-Warning "Failed to locate docs directory in downloaded repository."
}

# Clean temporary archive files
Remove-Item -Force $zipPath
Remove-Item -Force -Recurse $extractPath

# ------------------------------------------------------------------------------
# STEP 4: Build and Launch Docker Container
# ------------------------------------------------------------------------------
Write-Host "`n[4/4] Building and starting PocketBase container..." -ForegroundColor Cyan
docker compose up -d --build
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to start Docker Compose. Please verify Docker Desktop is running."
    exit
}

# Wait for container startup
Start-Sleep -Seconds 3

# ------------------------------------------------------------------------------
# SETUP COMPLETE
# ------------------------------------------------------------------------------
# Admin account and collections are created automatically by the PocketBase migrations on startup
$adminEmail = "service@datadunkers.ca"
$adminPass = "datadunkers"

$localIp = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias 'Wi-Fi','Ethernet' \vert{} Where-Object {$_.IPAddress -notlike "169.254.*"} | Select-Object -First 1).IPAddress

Write-Host "`n=================================================================" -ForegroundColor Green
Write-Host "SETUP COMPLETE!" -ForegroundColor Green
Write-Host "Web Server URL (LAN):  http://$localIp" -ForegroundColor White
Write-Host "PocketBase Admin UI:   http://$localIp/_/" -ForegroundColor White
Write-Host "Admin Credentials:     $adminEmail / $adminPass" -ForegroundColor White
Write-Host "=================================================================`n" -ForegroundColor Green