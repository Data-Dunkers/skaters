#!/usr/bin/env bash
# ==============================================================================
# DATA DUNKERS - AUTOMATED POCKETBASE & LAN SERVER SETUP (Linux / Raspberry Pi)
# ==============================================================================

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
WHITE='\033[1;37m'
NC='\033[0m'

log()  { echo -e "${2:-$NC}$1${NC}"; }

# Ensure script is running as root
if [ "$(id -u)" -ne 0 ]; then
    log "Please re-run this script with sudo/root (e.g. sudo ./linux-setup.sh)." "$RED"
    exit 1
fi

# Install Docker Engine + Compose plugin
log "\n[1/4] Checking Docker installation..." "$CYAN"
if ! command -v docker >/dev/null 2>&1; then
    log "Docker not found. Installing via get.docker.com..." "$YELLOW"
    curl -fsSL https://get.docker.com -o /tmp/get-docker.sh
    sh /tmp/get-docker.sh
    rm -f /tmp/get-docker.sh

    # Allow the invoking (non-root) user to run docker without sudo
    if [ -n "${SUDO_USER:-}" ]; then
        usermod -aG docker "$SUDO_USER" || true
        log "Added $SUDO_USER to the docker group. You may need to log out and back in for this to take effect." "$YELLOW"
    fi
else
    log "Docker is already installed." "$GREEN"
fi

if ! docker compose version >/dev/null 2>&1; then
    log "Docker Compose plugin not found. Installing..." "$YELLOW"
    apt-get update -y
    apt-get install -y docker-compose-plugin
fi
log "Docker and Docker Compose are ready." "$GREEN"

# Make sure the Docker daemon is running
if ! systemctl is-active --quiet docker; then
    log "Starting Docker service..." "$YELLOW"
    systemctl enable --now docker
fi
log "Docker service is running." "$GREEN"

# Configure firewall for port 80
log "\n[2/4] Configuring firewall..." "$CYAN"
if command -v ufw >/dev/null 2>&1; then
    ufw allow 80/tcp >/dev/null 2>&1 || true
    log "Inbound firewall rule ensured for TCP Port 80 (ufw)." "$GREEN"
else
    log "ufw not found, skipping firewall configuration. Ensure port 80 is reachable on your network." "$YELLOW"
fi

# Setup Project Directory Structure & Download Files from GitHub
log "\n[3/4] Setting up project folder structure..." "$CYAN"
projectDir="/opt/my-lan-app"
mkdir -p "$projectDir/pb_data" "$projectDir/pb_public"
cd "$projectDir"

log "Fetching setup files from GitHub..." "$CYAN"
zipPath="/tmp/skaters_repo.zip"
extractPath="/tmp/skaters_repo_extracted"

# Clean up previous downloads if existing
rm -f "$zipPath"
rm -rf "$extractPath"

curl -fsSL "https://github.com/Data-Dunkers/skaters/archive/refs/heads/main.zip" -o "$zipPath"
mkdir -p "$extractPath"
unzip -q -o "$zipPath" -d "$extractPath"
repoRoot="$extractPath/skaters-main"

# Copy Dockerfile, docker-compose.yaml and pb_migrations from /setup
setupPath="$repoRoot/setup"
if [ -d "$setupPath" ]; then
    cp -f "$setupPath/Dockerfile" "$projectDir/Dockerfile"
    cp -f "$setupPath/docker-compose.yaml" "$projectDir/docker-compose.yml"
    rm -rf "$projectDir/pb_migrations"
    cp -rf "$setupPath/pb_migrations" "$projectDir/pb_migrations"
    log "Downloaded Dockerfile, docker-compose.yml and pb_migrations from GitHub." "$GREEN"
else
    log "Failed to locate setup directory in downloaded repository." "$YELLOW"
fi

# Copy files from /docs to pb_public
docsPath="$repoRoot/docs"
if [ -d "$docsPath" ]; then
    cp -rf "$docsPath/." "$projectDir/pb_public/"
    log "Successfully downloaded and extracted static files to pb_public." "$GREEN"
else
    log "Failed to locate docs directory in downloaded repository." "$YELLOW"
fi

# Clean temporary archive files
rm -f "$zipPath"
rm -rf "$extractPath"

# Build and Launch Docker Container
log "\n[4/4] Building and starting PocketBase container..." "$CYAN"
docker compose up -d --build

# Wait for container startup
sleep 3

# Admin account and collections are created automatically by the PocketBase migrations on startup
adminEmail="service@datadunkers.ca"
adminPass="datadunkers"

localIp=$(hostname -I 2>/dev/null | awk '{print $1}')

log "\n=================================================================" "$GREEN"
log "SETUP COMPLETE!" "$GREEN"
log "Web Server URL (LAN):  http://$localIp" "$WHITE"
log "PocketBase Admin UI:   http://$localIp/_/" "$WHITE"
log "Admin Credentials:     $adminEmail / $adminPass" "$WHITE"
log "=================================================================\n" "$GREEN"
