# CDK Deployment Guide

This guide covers AWS CDK deployments using Ansible automation.

## Prerequisites

1. **Environment Setup**: Complete setup using one of these methods:
   - WSL: `./wsl-bootstrap.sh` + `ansible-playbook wsl-aws-auth.yml`
   - Linux: `ansible-playbook linux-setup.yml` + `ansible-playbook linux-aws-auth.yml`
   - Docker: `.\docker-bootstrap.ps1` + `.\run-docker.bat auth`

2. **AWS Authentication**: Ensure AWS SSO login is active
   ```bash
   aws sts get-caller-identity  # Should return your account info
   ```

## Available CDK Stacks

### 1. S3 Bucket Stack (`app.py`)

**Deploy:**
```bash
ansible-playbook cdk-simple.yml
```

**What it creates:**
- S3 bucket with versioning enabled
- Auto-delete objects on stack destruction
- Bucket name: `{config.bucket_name}-{account_id}-{region}`

**Configuration:** Edit `config.yml`:
```yaml
cdk:
  bucket_name: "my-project-bucket"
  region: "eu-central-1"
  account_id: "750246861878"
  profile: "default"
```

### 2. IAM Policy and Role Stack (`iam-app.py`)

**Deploy:**
```bash
ansible-playbook iam-deploy.yml
```

**Interactive prompts:**
1. IAM policy name
2. IAM role name  
3. S3 bucket name (for policy permissions)

**What it creates:**
- IAM managed policy with S3 GetObject/PutObject permissions
- IAM role for Lambda service with policy attached
- Outputs: Policy ARN and Role ARN

## Deployment Process

### Step-by-Step Deployment

1. **Bootstrap CDK** (first time only):
   ```bash
   cdk bootstrap aws://ACCOUNT_ID/REGION --profile default
   ```

2. **Deploy S3 Stack**:
   ```bash
   ansible-playbook cdk-simple.yml
   ```

3. **Deploy IAM Stack**:
   ```bash
   ansible-playbook iam-deploy.yml
   # Follow prompts for names
   ```

4. **View Outputs**:
   ```bash
   cat cdk-outputs.json     # S3 stack outputs
   cat iam-outputs.json     # IAM stack outputs
   ```

### Destroy Resources

**Destroy specific stack:**
```bash
# S3 stack
cdk destroy --profile default --app "python3 app.py" --force

# IAM stack  
cdk destroy --profile default --app "python3 iam-app.py" --force
```

**Destroy all via Ansible:**
```bash
ansible-playbook cdk-destroy.yml
```

## File Structure

```
ansible/
├── app.py              # S3 bucket CDK app
├── iam-app.py          # IAM policy/role CDK app
├── cdk.json            # CDK config for app.py
├── iam-cdk.json        # CDK config for iam-app.py
├── requirements.txt    # Python dependencies
├── config.yml          # Ansible/CDK configuration
├── cdk-simple.yml      # S3 deployment playbook
├── iam-deploy.yml      # IAM deployment playbook
└── cdk-destroy.yml     # Destruction playbook
```

## Troubleshooting

### Common Issues

**1. Credentials not found:**
```
Unable to retrieve credentials: The config profile (default) could not be found
```
**Solution:** Run AWS SSO login:
```bash
aws sso login --profile default
```

**2. Bootstrap required:**
```
SSM parameter /cdk-bootstrap/hnb659fds/version not found
```
**Solution:** Bootstrap the region:
```bash
cdk bootstrap aws://ACCOUNT_ID/REGION --profile default
```

**3. Bucket name conflicts:**
```
Bucket name must be globally unique
```
**Solution:** Change bucket name in `config.yml` or use the auto-generated suffix.

**4. File not found:**
```
python3: can't open file 'iam-app.py': No such file or directory
```
**Solution:** Run playbook from the correct directory (ansible/).

### Verification Commands

```bash
# Check AWS authentication
aws sts get-caller-identity --profile default

# List CDK stacks
cdk list --profile default --app "python3 app.py"
cdk list --profile default --app "python3 iam-app.py"

# Check CloudFormation stacks
aws cloudformation list-stacks --profile default

# Verify S3 bucket
aws s3 ls --profile default

# Verify IAM resources
aws iam list-roles --profile default
aws iam list-policies --scope Local --profile default
```

## Best Practices

1. **Use unique names** for policies and roles to avoid conflicts
2. **Test in development** account before production
3. **Review outputs** after deployment to verify resources
4. **Clean up resources** when no longer needed to avoid costs
5. **Use version control** for CDK code changes
6. **Document custom configurations** in your project

## Advanced Usage

### Custom CDK Apps

Create new CDK applications following the pattern:

1. **Create CDK app** (`my-app.py`)
2. **Create CDK config** (`my-cdk.json`)
3. **Create Ansible playbook** (`my-deploy.yml`)
4. **Update configuration** (`config.yml`)

### Environment Variables

CDK apps can use environment variables for dynamic configuration:

```python
# In your CDK app
import os
resource_name = os.environ.get('RESOURCE_NAME', 'default-name')
```

```yaml
# In Ansible playbook
environment:
  RESOURCE_NAME: "{{ user_input.user_input }}"
```

This pattern enables flexible, reusable infrastructure deployments.