#!/bin/bash

set -o errexit
set -o pipefail

#####################
### MAIN FUNCTION ###
#####################

main() {
    echo
    echo "Checking for root or sudo..."
    check_root
    echo "Detecting OS..."
    detect_os
    echo "OS detected: $os"
    echo

    install_all_the_dependencies
    echo

    install_python
    echo

    install_nodejs
    echo

    install_npm
    echo

    install_aws_cdk
    echo

    python_env_setup
    echo

    echo "Setup completed successfully."
}

########################
### BASE FUNCTIONS   ###
########################

check_root() {
    if [[ $EUID -ne 0 ]]; then
        SUDO='sudo -E'
    else
        SUDO=''
    fi
}

detect_os() {
    if grep -qs "ubuntu" /etc/os-release; then
        os="ubuntu"
        os_version=$(grep 'VERSION_ID' /etc/os-release | cut -d '"' -f 2 | tr -d '.')
        if [[ "$os_version" -lt 2004 ]]; then
            echo "Use Ubuntu 20.04 or higher."
            exit 1
        fi
    elif [[ -e /etc/debian_version ]]; then
        os="debian"
        os_version=$(grep -oE '[0-9]+' /etc/debian_version | head -1)
        if [[ "$os_version" -lt 11 ]]; then
            echo "Use Debian 11 or higher."
            exit 1
        fi
    else
        echo "Unsupported OS: $(uname -a)"
        exit 1
    fi
}

#######################################
### INSTALLATION FUNCTIONS (UBU/DEB) ###
#######################################

install_packages_debian_ubuntu() {
    REQUIRED_PACKAGES=(
        net-tools
        sudo
        curl
        wget
        git
        unzip
        rsync
        zip
        ca-certificates
    )

    echo "Installing system dependencies..."
    $SUDO apt update -y
    $SUDO apt-get -o Dpkg::Options::="--force-confold" -fuy install "${REQUIRED_PACKAGES[@]}"
    echo "Dependencies installed."
}

install_all_the_dependencies() {
    install_packages_debian_ubuntu
}

###################################
### PYTHON + AWS CLI INSTALLERS ###
###################################

install_python() {
    echo "Installing Python + pip + venv..."
    $SUDO apt install -y python3 python3-venv python3-pip python3-setuptools
    echo "Python installation complete."
}

install_awscli() {
    echo "Installing AWS CLI v2..."
    curl -s "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip -q awscliv2.zip
    $SUDO ./aws/install --bin-dir /usr/local/bin --install-dir /usr/local/aws-cli --update
    rm -rf aws awscliv2.zip
    echo "AWS CLI installed."
}

####################################
### NODEJS / NPM / AWS-CDK SETUP ###
####################################

install_nodejs() {
    echo "Installing Node.js LTS (via Nodesource)..."
    curl -fsSL https://deb.nodesource.com/setup_lts.x | $SUDO bash -
    $SUDO apt install -y nodejs
    echo "Node.js installed: $(node -v)"
}

install_npm() {
    echo "Ensuring npm is installed..."
    if ! command -v npm >/dev/null 2>&1; then
        echo "npm not found, reinstalling nodejs..."
        $SUDO apt install -y npm
    fi
    echo "npm installed: $(npm -v)"
}

install_aws_cdk() {
    echo "Installing AWS CDK..."
    $SUDO npm install -g aws-cdk
    echo "AWS CDK installed: $(cdk --version)"
}

######################################
### PYTHON VENV + REQUIREMENTS SETUP ###
######################################

python_env_setup() {
    echo "Creating Python virtual environment..."

    if [[ ! -d ".venv" ]]; then
        python3 -m venv .venv
    fi

    echo "Activating virtual environment..."
    # shellcheck disable=SC1091
    source .venv/bin/activate

    echo "Updating pip..."
    pip install --upgrade pip

    if [[ -f "requirements.txt" ]]; then
        echo "Installing requirements..."
        pip install -r requirements.txt
    else
        echo "requirements.txt not found, skipping."
    fi
    exit 1
}

main "$@"
