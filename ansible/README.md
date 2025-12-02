# Ansible Pre-Deployment Setup

Automated setup playbooks for AWS infrastructure deployment across Linux systems and WSL (Ubuntu/Debian).
Includes CDK deployment automation for S3 buckets, IAM policies, and roles.

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

### WSL (Ubuntu/Debian)

**Control Machine:**
- Windows 10/11 with WSL2 enabled
- Python 3.6+
- Ansible + pexpect (see prerequisites above)

**Target WSL Instances:**
- Ubuntu 20.04+ or Debian 11+ on WSL
- SSH server configured (optional for remote access)
- User with sudo privileges

**Setup WSL for automation:**
```powershell
# Step 1: Install WSL (run as Administrator)
.\wsl-installation.ps1

# Step 2: After reboot, launch WSL and run:
```
```bash
# Inside WSL terminal
./wsl-bootstrap.sh
```

### Docker Desktop (Windows)

**Control Machine:**
- Windows 10/11 with Docker Desktop
- Docker Desktop running
- No additional Python/Ansible installation required

**Setup Docker environment:**
```powershell
# Run bootstrap script
.\docker-bootstrap.ps1

# Quick commands
.\run-docker.bat auth    # AWS SSO login
.\run-docker.bat shell   # Interactive shell
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

[wsl]
wsl-ubuntu ansible_host=localhost ansible_user=ubuntu ansible_connection=local ansible_python_interpreter=/usr/bin/python3
wsl-debian ansible_host=localhost ansible_user=debian ansible_connection=local ansible_python_interpreter=/usr/bin/python3

[docker]
localhost ansible_connection=local
```


## CDK Deployments

After environment setup, deploy AWS infrastructure:

### S3 Bucket Stack
```bash
ansible-playbook cdk-simple.yml
```
- Creates S3 bucket with versioning
- Uses configuration from `config.yml`
- Outputs bucket name and ARN

### IAM Policy and Role Stack
```bash
ansible-playbook iam-deploy.yml
```
- Prompts for policy name, role name, and bucket name
- Creates IAM policy with S3 permissions
- Creates IAM role with policy attached
- Outputs policy and role ARNs

### Destroy Resources
```bash
ansible-playbook cdk-destroy.yml
```
- Destroys CDK stacks and resources
- Automatically handles S3 object deletion

### CDK Configuration

Edit `config.yml` for CDK settings:
```yaml
cdk:
  region: "eu-central-1"
  bucket_name: "cb-project-bucket"
  stack_name: "CBProjectStack"
  account_id: "750246861878"
  profile: "default"
```

## What Gets Installed

### Linux
- System packages (curl, git, unzip, etc.)
- Python 3 + pip + venv
- AWS CLI v2
- Node.js LTS
- AWS CDK
- Python virtual environment

### WSL (Ubuntu/Debian)
- System packages (curl, git, unzip, build-essential)
- Python 3 + pip + venv
- AWS CLI v2
- Node.js LTS (via NodeSource)
- AWS CDK
- Python virtual environment
- WSL-specific optimizations

### Docker Desktop
- Containerized Ansible environment
- AWS CLI v2
- Python 3 + pip
- Shared AWS credentials with host

## Troubleshooting

**Linux SSH issues:**
```bash
# Test SSH connection
ssh -i ~/.ssh/id_rsa user@server-ip

# Check SSH agent
ssh-add ~/.ssh/id_rsa
```

**WSL connection issues:**
```bash
# Test WSL connection
ansible wsl -m ping

# Check WSL status
wsl --list --verbose

# Restart WSL if needed
wsl --shutdown
wsl -d Ubuntu  # or Debian
```

**Docker issues:**
```bash
# Check Docker status
docker version

# Rebuild container
docker-compose build --no-cache

# Check AWS credentials mount
docker-compose run --rm ansible ls -la /root/.aws
```

**Permission errors:**
- Ensure user has sudo privileges (Linux/WSL)
- Run commands from elevated PowerShell if accessing WSL from Windows
- Ensure Docker Desktop has access to C: drive (Docker settings)