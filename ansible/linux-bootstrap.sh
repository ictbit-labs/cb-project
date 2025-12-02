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
sudo apt install -y ansible python3-pexpect

# Verify installation
echo "Verifying installation..."
ansible --version
python3 --version

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
echo "1. Run setup: ansible-playbook linux-setup.yml -v"
echo ""
echo "2. Configure AWS SSO:"
echo "   aws configure sso --no-browser"
echo ""
echo "   Enter these values when prompted:"
echo "   • SSO session name: default"
echo "   • SSO start URL: https://d-<YOUR_NUMBER>.awsapps.com/start"
echo "   • SSO region: <SSO_REGION>"
echo "   • SSO registration scopes: [press ENTER for default]"
echo "   • CLI default client Region: <REGION>"
echo "   • CLI default output format: json"
echo ""
echo "3. Login to AWS SSO:"
echo "   aws sso login --profile default"
echo ""
echo "4. Verify authentication:"
echo "   aws sts get-caller-identity --profile default"
echo ""
echo "WSL environment is ready"