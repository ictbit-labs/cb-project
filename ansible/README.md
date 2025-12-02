# Ansible Pre-Deployment Setup

Automated setup playbooks for AWS infrastructure deployment across Linux and Windows systems.

## Requirements

### Prerequisites

**Install before running playbooks:**
```bash
pip install ansible pexpect pywinrm
```

### Linux (Ubuntu/Debian)

**Control Machine:**
- Python 3.6+
- Ansible + pexpect (see prerequisites above)
- SSH access to target servers (for remote)

**Target Servers:**
- Ubuntu 20.04+ or Debian 11+
- SSH server running
- User with sudo privileges

**Setup SSH access:**
```bash
# Generate SSH key if needed
ssh-keygen -t rsa -b 4096

# Copy public key to target server
ssh-copy-id user@server-ip
```

### Windows

**Control Machine:**
- Python 3.6+
- Ansible + pexpect + pywinrm (see prerequisites above)

**Target Servers:**
- Windows 10/Server 2016+
- PowerShell 3.0+
- WinRM enabled

**Enable WinRM on Windows:**
```powershell
# Run as Administrator
winrm quickconfig -y
winrm set winrm/config/service/auth '@{Basic="true"}'
winrm set winrm/config/service '@{AllowUnencrypted="true"}'
```

## Configuration

### AWS SSO Setup

Edit `config.yml` with your AWS SSO details:

```yaml
aws_sso:
  start_url: "https://d-9067d191db.awsapps.com/start"
  region: "us-east-1"
  profile_name: "default"
  session_name: "default"
  cli_region: "eu-central-1"
  output_format: "json"
```



### Inventory Setup

Edit `inventory.ini`:

```ini
[local]
localhost ansible_connection=local

[remote]
ubuntu-server ansible_host=192.168.1.100 ansible_user=ubuntu ansible_ssh_private_key_file=~/.<PATH>>

[windows]
win-server ansible_host=192.168.1.200 ansible_user=Administrator ansible_password=SecurePass123 ansible_connection=winrm ansible_winrm_transport=basic
```


## What Gets Installed

### Linux
- System packages (curl, git, unzip, etc.)
- Python 3 + pip + venv
- AWS CLI v2
- Node.js LTS
- AWS CDK
- Python virtual environment

### Windows
- Chocolatey package manager
- Git, curl, wget, 7zip
- Python 3
- AWS CLI v2
- Node.js LTS
- AWS CDK
- Python virtual environment

## Troubleshooting

**Linux SSH issues:**
```bash
# Test SSH connection
ssh -i ~/.ssh/id_rsa user@server-ip

# Check SSH agent
ssh-add ~/.ssh/id_rsa
```

**Windows WinRM issues:**
```bash
# Test WinRM connection
ansible windows -m win_ping
```

**Permission errors:**
- Ensure user has sudo privileges (Linux)
- Run PowerShell as Administrator (Windows)