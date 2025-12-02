#!/bin/bash
# WSL Bootstrap Script for CB Project
# Run this script to quickly set up your WSL environment

set -e

echo "=== WSL Bootstrap ==="
echo "Setting up WSL Ubuntu/Debian environment..."

# Check if running in WSL
if ! grep -qi microsoft /proc/version 2>/dev/null; then
    echo "Warning: This script is optimized for WSL environments"
fi

# Update system (check if recently updated)
echo "Updating system packages..."
if [ ! -f /var/lib/apt/periodic/update-success-stamp ] || [ $(find /var/lib/apt/periodic/update-success-stamp -mtime +1) ]; then
    sudo apt update && sudo apt upgrade -y
else
    echo "System packages recently updated, skipping..."
fi

# Install Ansible if not present
if ! command -v ansible &> /dev/null; then
    echo "Installing Ansible..."
    sudo apt install -y ansible python3-pexpect dos2unix
fi



# Verify ansible installation
if command -v ansible &> /dev/null; then
    echo "Ansible installed successfully: $(ansible --version | head -1)"
else
    echo "Warning: Ansible installation may have failed"
fi

echo ""
echo "=== Bootstrap Complete ==="
echo "Next steps:"
echo "1. Run setup: ansible-playbook wsl-setup.yml -v"
echo "2. Configure AWS SSO:"
echo "   aws configure sso --profile default --no-browser"
echo "   Then: aws sso login --profile default"
echo ""
echo "WSL environment is ready"