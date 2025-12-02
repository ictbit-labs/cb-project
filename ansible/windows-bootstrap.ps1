# Windows Bootstrap Script - Run this first on new Windows machine

Write-Host "Installing Python and Ansible on Windows..." -ForegroundColor Green

# Python installer URL (change version if needed)
$pythonUrl = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"
$pythonInstaller = "$env:TEMP\python-installer.exe"

# Download Python installer
Write-Host "Downloading Python installer..." -ForegroundColor Yellow
Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonInstaller

# Install Python silently
Write-Host "Installing Python silently..." -ForegroundColor Blue
Start-Process $pythonInstaller -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 Include_pip=1" -Wait

Start-Sleep -Seconds 5

# Locate python.exe (avoid Windows Store stub)
Write-Host "Searching for Python installation..." -ForegroundColor Yellow

# Search in common installation paths first
$PythonPaths = @(
    "C:\Program Files\Python*\python.exe",
    "C:\Program Files (x86)\Python*\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python*\python.exe"
)

$PythonExe = $null
foreach ($path in $PythonPaths) {
    $found = Get-ChildItem $path -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($found) {
        $PythonExe = $found
        break
    }
}

if (-not $PythonExe) {
    Write-Host "ERROR: Python installation not found after silent install!" -ForegroundColor Red
    Write-Host "Please check if Python was installed correctly." -ForegroundColor Red
    exit 1
}

$Py = $PythonExe.FullName
Write-Host "Using Python at: $Py" -ForegroundColor Green

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Blue
& $Py -m pip install --upgrade pip

# Install Ansible + Dependencies
Write-Host "Installing Ansible + dependencies..." -ForegroundColor Blue
& $Py -m pip install ansible pywinrm pexpect

# Look for ansible.exe
$ScriptsDir = Split-Path $Py | Join-Path -ChildPath "Scripts"
$AnsibleExe = Join-Path $ScriptsDir "ansible.exe"

Write-Host "Verifying installation..." -ForegroundColor Blue
& $Py --version
& $Py -m pip --version

if (Test-Path $AnsibleExe) {
    try {
        & $AnsibleExe --version
    } catch {
        Write-Host "Ansible installed but executable has permission issues (this is normal)" -ForegroundColor Yellow
        Write-Host "You can still run playbooks with: ansible-playbook" -ForegroundColor Green
    }
} else {
    Write-Host "WARNING: ansible.exe not found in $ScriptsDir" -ForegroundColor Yellow
}

Write-Host "`nBootstrap completed!" -ForegroundColor Green
Write-Host "You can now run:"
Write-Host "  .\run.ps1 windows-setup" -ForegroundColor Cyan
Write-Host "  .\run.ps1 windows-auth" -ForegroundColor Cyan