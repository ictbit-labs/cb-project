#!/bin/bash

echo "Installing Python and Ansible on Linux..."

# Update package manager
sudo apt update

# Install Python and pip if not present
if ! command -v python3 &> /dev/null; then
    echo "Installing Python..."
    sudo apt install -y python3 python3-pip python3-venv
else
    echo "Python already installed: $(python3 --version)"
fi

# Install Ansible and all dependencies needed for playbooks
echo "Installing Ansible and dependencies..."
pip install ansible pywinrm pexpect

# Verify installation
echo "Verifying installation..."
ansible --version
python3 --version

echo "Bootstrap completed! You can now run:"
echo "  ./run.sh linux-setup"
echo "  ./run.sh linux-auth"
echo "  ./run.sh linux        # (both)"