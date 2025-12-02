# Testing Guide

## Windows Testing (Fresh OS)

### Step 1: Bootstrap (Install Ansible)
```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\windows-bootstrap.ps1
```

### Step 2: Configure AWS SSO
Edit `config.yml` with your values:
```yaml
aws_sso:
  start_url: "https://your-org.awsapps.com/start"
  region: "us-east-1"
  profile_name: "default"
  session_name: "default"
  cli_region: "eu-central-1"
  output_format: "json"
```

### Step 3: Run Setup
```powershell
# Install software only
.\run.ps1 windows-setup

# Configure AWS (interactive)
.\run.ps1 windows-auth

# Or run both
.\run.ps1 windows
```

## Linux Testing (Fresh OS)

### Step 1: Bootstrap (Install Ansible)
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3 python3-pip
pip install ansible pexpect pywinrm
```

### Step 2: Configure AWS SSO
Edit `config.yml` (same as Windows)

### Step 3: Run Setup
```bash
# Install software only
./run.sh linux-setup

# Configure AWS (automated)
./run.sh linux-auth

# Or run both
./run.sh linux
```

## Verification Commands

After setup, verify everything works:

```bash
# Check installations
aws --version
node --version
cdk --version
python3 --version

# Check AWS authentication
aws sts get-caller-identity --profile default

# Check CDK
cdk --version
```

## Troubleshooting

**Windows PowerShell execution policy:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Linux permission issues:**
```bash
chmod +x run.sh
```

**AWS SSO issues:**
- Ensure correct start_url in config.yml
- Complete browser authentication when prompted
- Check profile with: `aws configure list-profiles`