# Docker Desktop Bootstrap Script for CB Project
# Requires Docker Desktop to be installed and running

Write-Host "Setting up CB Project with Docker Desktop..." -ForegroundColor Green

# Check if Docker is running
try {
    docker version | Out-Null
} catch {
    Write-Host "ERROR: Docker Desktop is not running!" -ForegroundColor Red
    Write-Host "Please start Docker Desktop and try again." -ForegroundColor Yellow
    exit 1
}

# Build the Ansible container
Write-Host "Building Ansible container..." -ForegroundColor Blue
docker-compose build

# Create AWS credentials directory if it doesn't exist
$awsDir = "$env:USERPROFILE\.aws"
if (-not (Test-Path $awsDir)) {
    New-Item -ItemType Directory -Path $awsDir -Force
    Write-Host "Created AWS credentials directory: $awsDir" -ForegroundColor Yellow
}

Write-Host "`n=== Docker Setup Complete ===" -ForegroundColor Green
Write-Host "Usage:" -ForegroundColor Cyan
Write-Host "  docker-compose run --rm ansible ansible-playbook docker-aws-auth.yml" -ForegroundColor White
Write-Host "  docker-compose run --rm ansible bash" -ForegroundColor White

Write-Host "`nDocker environment ready for AWS SSO authentication!" -ForegroundColor Green