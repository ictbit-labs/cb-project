# CB Project

This is an automation project utilizing Ansible, AWS CDK, and Terraform for infrastructure management and deployment.

## Project Components

### Ansible
Contains automated setup playbooks for AWS infrastructure deployment across Linux systems and WSL (Ubuntu/Debian).
Includes CDK deployment automation for S3 buckets, IAM policies, and roles.
For detailed instructions, please refer to the [Ansible README](ansible/README.md).

### AWS CDK
Python-based CDK applications for infrastructure deployment:
- **S3 Bucket Stack** (`app.py`) - Creates S3 buckets with versioning
- **IAM Stack** (`iam-app.py`) - Creates IAM policies and roles with dynamic inputs

### Terraform
Contains Infrastructure as Code (IaC) definitions for provisioning cloud resources.

## Getting Started

**Quick Setup:** See [SETUP-GUIDE.md](SETUP-GUIDE.md) for detailed instructions

**Fast Track:** See [ansible/QUICK-START.md](ansible/QUICK-START.md) for minimal steps

## CDK Deployments

After environment setup:

```bash
# Deploy S3 bucket
ansible-playbook ansible/cdk-simple.yml

# Deploy IAM policy and role (with prompts)
ansible-playbook ansible/iam-deploy.yml

# Destroy resources
ansible-playbook ansible/cdk-destroy.yml
```

Please check the respective subdirectories for specific setup and usage instructions.