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
Write-Host "`n[1/6] Checking WSL 2 installation status..." -ForegroundColor Cyan
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
Write-Host "`n[2/6] Configuring Firewall and Network Profile..." -ForegroundColor Cyan

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
# STEP 3: Setup Project Directory Structure & Docker Files
# ------------------------------------------------------------------------------
Write-Host "`n[3/6] Setting up project folder structure..." -ForegroundColor Cyan
$projectDir = "C:\my-lan-app"
New-Item -ItemType Directory -Force -Path "$projectDir\pb_data" | Out-Null
New-Item -ItemType Directory -Force -Path "$projectDir\pb_public" | Out-Null
Set-Location -Path $projectDir

# Create Dockerfile
$dockerfileContent = @"
FROM alpine:latest

ARG PB_VERSION=0.22.21

RUN apk add --no-cache ca-certificates unzip wget curl

ADD https://github.com/pocketbase/pocketbase/releases/download/v`${PB_VERSION}/pocketbase_`${PB_VERSION}_linux_amd64.zip /tmp/pb.zip
RUN unzip /tmp/pb.zip -d /pb/ \
    && rm /tmp/pb.zip \
    && chmod +x /pb/pocketbase

EXPOSE 8090

CMD ["/pb/pocketbase", "serve", "--http=0.0.0.0:8090", "--dir=/pb/pb_data", "--publicDir=/pb/pb_public"]
"@
Set-Content -Path "$projectDir\Dockerfile" -Value $dockerfileContent

# Create docker-compose.yml
$composeContent = @"
services:
  pocketbase:
    build: .
    container_name: lan_pocketbase
    restart: unless-stopped
    ports:
      - "80:8090"
    volumes:
      - ./pb_data:/pb/pb_data
      - ./pb_public:/pb/pb_public
"@
Set-Content -Path "$projectDir\docker-compose.yml" -Value $composeContent
Write-Host "Project configuration files created at $projectDir" -ForegroundColor Green

# ------------------------------------------------------------------------------
# STEP 4: Download and Extract GitHub docs to pb_public
# ------------------------------------------------------------------------------
Write-Host "`n[4/6] Fetching static web assets from GitHub..." -ForegroundColor Cyan
$zipPath = "$env:TEMP\skaters_repo.zip"
$extractPath = "$env:TEMP\skaters_repo_extracted"

# Clean up previous downloads if existing
if (Test-Path $zipPath) { Remove-Item -Force $zipPath }
if (Test-Path $extractPath) { Remove-Item -Force -Recurse $extractPath }

Invoke-WebRequest -Uri "https://github.com/Data-Dunkers/skaters/archive/refs/heads/main.zip" -OutFile $zipPath
Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force

# Copy files from /docs to pb_public
$docsPath = "$extractPath\skaters-main\docs"
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
# STEP 5: Build and Launch Docker Container
# ------------------------------------------------------------------------------
Write-Host "`n[5/5] Building and starting PocketBase container..." -ForegroundColor Cyan
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