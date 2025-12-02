# WSL Bootstrap Script - Run this first on Windows to set up WSL
# This script must be run as Administrator

Write-Host "Setting up WSL (Windows Subsystem for Linux)..." -ForegroundColor Green

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

# Check Windows version
$WindowsVersion = [System.Environment]::OSVersion.Version
if ($WindowsVersion.Major -lt 10 -or ($WindowsVersion.Major -eq 10 -and $WindowsVersion.Build -lt 19041)) {
    Write-Host "ERROR: WSL 2 requires Windows 10 version 2004 or higher" -ForegroundColor Red
    exit 1
}

# Enable WSL feature
Write-Host "Enabling WSL feature..." -ForegroundColor Blue
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# Enable Virtual Machine Platform
Write-Host "Enabling Virtual Machine Platform..." -ForegroundColor Blue
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Download and install WSL2 Linux kernel update
Write-Host "Downloading WSL2 Linux kernel update..." -ForegroundColor Yellow
$kernelUrl = "https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi"
$kernelInstaller = "$env:TEMP\wsl_update_x64.msi"

try {
    Invoke-WebRequest -Uri $kernelUrl -OutFile $kernelInstaller
    Write-Host "Installing WSL2 kernel update..." -ForegroundColor Blue
    Start-Process msiexec.exe -ArgumentList "/i $kernelInstaller /quiet" -Wait
} catch {
    Write-Host "Warning: Could not download kernel update. You may need to install it manually." -ForegroundColor Yellow
}

# Set WSL 2 as default version
Write-Host "Setting WSL 2 as default version..." -ForegroundColor Blue
wsl --set-default-version 2

# Install Ubuntu (default distribution)
Write-Host "Installing Ubuntu distribution..." -ForegroundColor Blue
try {
    wsl --install -d Ubuntu --no-launch
} catch {
    Write-Host "Installing Ubuntu via Microsoft Store method..." -ForegroundColor Yellow
    # Alternative method using winget if available
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        winget install Canonical.Ubuntu
    } else {
        Write-Host "Please install Ubuntu manually from Microsoft Store" -ForegroundColor Red
    }
}

# Check if reboot is required
$rebootRequired = $false
try {
    $pendingReboot = Get-ChildItem "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired" -ErrorAction SilentlyContinue
    if ($pendingReboot) { $rebootRequired = $true }
} catch { }

Write-Host "`n=== WSL Installation Complete ===" -ForegroundColor Green

if ($rebootRequired) {
    Write-Host "REBOOT REQUIRED: Please restart your computer to complete WSL installation" -ForegroundColor Red
    Write-Host "After reboot, run: wsl" -ForegroundColor Yellow
} else {
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Launch WSL: wsl" -ForegroundColor White
    Write-Host "2. Set up user account when prompted" -ForegroundColor White
    Write-Host "3. Run the WSL bootstrap: ./wsl-bootstrap.sh" -ForegroundColor White
    Write-Host "4. Configure AWS: ansible-playbook wsl-aws-auth.yml" -ForegroundColor White
}

Write-Host "`nWSL Ubuntu is ready" -ForegroundColor Green