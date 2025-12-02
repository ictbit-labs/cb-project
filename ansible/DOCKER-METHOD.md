# Docker Method Setup Guide

Complete guide for setting up and using the CB Project with Docker Desktop on Windows.

## Prerequisites

### Required Software
- **Windows 10/11** (Pro, Enterprise, or Education)
- **Docker Desktop** installed and running
- **Git** (optional, for cloning repository)

### Docker Desktop Setup
1. Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop/)
2. Install and restart Windows
3. Enable WSL 2 backend (recommended)
4. Ensure Docker Desktop is running (whale icon in system tray)

## Quick Start

### Step 1: Initial Setup
```cmd
cd ansible
.\docker-bootstrap.ps1
```

### Step 2: AWS Authentication
```cmd
.\run-docker.bat auth
```
Follow the prompts to configure AWS SSO and login.

### Step 3: Deploy Infrastructure
```cmd
# Deploy S3 bucket
.\run-docker.bat s3

# Deploy IAM policy and role (with prompts)
.\run-docker.bat iam

# Destroy resources when done
.\run-docker.bat destroy
```

## Detailed Setup Process

### 1. Environment Preparation

**Clone or navigate to project:**
```cmd
cd C:\path\to\cb-project\ansible
```

**Run bootstrap script:**
```cmd
.\docker-bootstrap.ps1
```

This script:
- Builds the Docker container with all dependencies
- Sets up volume mounts for AWS credentials
- Configures container networking

### 2. AWS Configuration

**Start authentication process:**
```cmd
.\run-docker.bat auth
```

**Interactive prompts will ask for:**
- AWS SSO Start URL (e.g., `https://d-xxxxxxxxxx.awsapps.com/start`)
- SSO Region (e.g., `us-east-1`)
- CLI Region (e.g., `eu-central-1`)
- Output format (e.g., `json`)

**Complete browser authentication:**
- Browser will open for AWS SSO login
- Sign in with your AWS credentials
- Return to terminal when complete

### 3. Verify Setup

**Test AWS connection:**
```cmd
.\run-docker.bat shell
aws sts get-caller-identity
exit
```

Should return your AWS account information.

## CDK Deployments

### S3 Bucket Stack

**Deploy:**
```cmd
.\run-docker.bat s3
```

**What it creates:**
- S3 bucket with versioning enabled
- Bucket name: `{config.bucket_name}-{account_id}-{region}`
- Auto-delete objects on destruction

**Configuration:** Edit `config.yml`:
```yaml
cdk:
  bucket_name: "my-project-bucket"
  region: "eu-central-1"
  account_id: "750246861878"
  profile: "default"
```

### IAM Policy and Role Stack

**Deploy:**
```cmd
.\run-docker.bat iam
```

**Interactive prompts:**
1. **IAM policy name** - Name for the managed policy
2. **IAM role name** - Name for the IAM role
3. **S3 bucket name** - Bucket for policy permissions

**What it creates:**
- IAM managed policy with S3 GetObject/PutObject permissions
- IAM role for Lambda service with policy attached
- Outputs: Policy ARN and Role ARN

### Destroy Resources

**Remove all CDK resources:**
```cmd
.\run-docker.bat destroy
```

This will:
- Delete S3 bucket and all objects
- Remove IAM policy and role
- Clean up CloudFormation stacks

## Available Commands

### Core Commands
```cmd
.\run-docker.bat auth      # AWS SSO authentication
.\run-docker.bat shell     # Interactive container shell
.\run-docker.bat s3        # Deploy S3 bucket stack
.\run-docker.bat iam       # Deploy IAM policy/role stack
.\run-docker.bat destroy   # Destroy all CDK resources
```

### Custom Playbooks
```cmd
.\run-docker.bat playbook <playbook-name.yml>
```

Examples:
```cmd
.\run-docker.bat playbook docker-cdk-simple.yml
.\run-docker.bat playbook custom-deployment.yml
```

## File Access

### Windows Directory Access
The container can access Windows directories at `/mnt/users/`:

```bash
# Inside container shell
ls /mnt/users/YourUsername/Desktop/
cat /mnt/users/YourUsername/Documents/file.txt
```

### Project Files
All project files are mounted at `/ansible/`:
```bash
# Inside container
ls /ansible/          # Project files
cat /ansible/config.yml
```

### AWS Credentials
AWS credentials are automatically mounted from Windows:
```bash
# Inside container
ls /root/.aws/        # AWS config and credentials
```

## Troubleshooting

### Docker Issues

**Container won't start:**
```cmd
# Check Docker Desktop status
docker version

# Rebuild container
docker-compose build --no-cache
```

**Permission errors:**
```cmd
# Ensure Docker Desktop has C: drive access
# Docker Desktop → Settings → Resources → File Sharing
```

**Container can't access AWS credentials:**
```cmd
# Check AWS directory exists
dir %USERPROFILE%\.aws

# Restart Docker Desktop
```

### AWS Authentication Issues

**SSO login fails:**
```cmd
# Clear existing credentials
del %USERPROFILE%\.aws\credentials
del %USERPROFILE%\.aws\config

# Re-run authentication
.\run-docker.bat auth
```

**Profile not found:**
```cmd
# Check AWS configuration
.\run-docker.bat shell
aws configure list-profiles
aws sts get-caller-identity --profile default
```

### CDK Deployment Issues

**Bootstrap required:**
```cmd
.\run-docker.bat shell
cdk bootstrap aws://ACCOUNT_ID/REGION --profile default
```

**Node.js/CDK not found:**
```cmd
# Rebuild container with latest dependencies
docker-compose build --no-cache
```

**File not found errors:**
```cmd
# Ensure you're in the ansible directory
cd C:\path\to\cb-project\ansible
.\run-docker.bat s3
```

## Advanced Usage

### Interactive Development

**Open container shell:**
```cmd
.\run-docker.bat shell
```

**Inside container:**
```bash
# Manual CDK commands
source .venv/bin/activate
cdk list
cdk synth
cdk deploy --profile default

# Manual Ansible commands
ansible-playbook cdk-simple.yml
ansible localhost -m setup
```

### Custom Configuration

**Edit configuration:**
```cmd
notepad config.yml
```

**Test configuration:**
```cmd
.\run-docker.bat shell
ansible-playbook --check cdk-simple.yml
```

### Container Management

**View running containers:**
```cmd
docker ps
```

**Stop container:**
```cmd
docker-compose down
```

**Remove container and rebuild:**
```cmd
docker-compose down
docker-compose build --no-cache
```

## Best Practices

### Security
- Never commit AWS credentials to version control
- Use AWS SSO instead of long-term access keys
- Regularly rotate credentials

### Development
- Test deployments in development account first
- Use unique resource names to avoid conflicts
- Clean up resources when no longer needed

### Performance
- Keep Docker Desktop updated
- Allocate sufficient resources (Settings → Resources)
- Use WSL 2 backend for better performance

### Maintenance
- Regularly update container dependencies
- Monitor Docker Desktop resource usage
- Clean up unused containers and images

## Container Details

### Installed Software
- **Python 3.11** with pip and venv
- **Ansible** with pexpect and boto3
- **AWS CLI v2** for AWS operations
- **Node.js LTS** for CDK runtime
- **AWS CDK CLI** for infrastructure deployment
- **Git** for version control
- **Build tools** for compilation

### Volume Mounts
- `.:/ansible` - Project files
- `~/.aws:/root/.aws` - AWS credentials
- `C:/Users:/mnt/users` - Windows user directories

### Environment Variables
- `AWS_PROFILE=default` - Default AWS profile

This Docker method provides a complete, isolated environment for AWS infrastructure deployment without requiring local installation of Python, Node.js, or AWS tools.