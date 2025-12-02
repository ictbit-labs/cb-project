# Quick Start Instructions

## For Windows Users

### Option A: Docker (Fastest)
1. Install Docker Desktop
2. Run: `.\docker-bootstrap.ps1`
3. Run: `.\run-docker.bat auth`

### Option B: WSL (Most Features)
1. Run as Admin: `.\wsl-installation.ps1`
2. Restart computer if prompted
3. In WSL: `./wsl-bootstrap.sh`
4. In WSL: `ansible-playbook wsl-aws-auth.yml`

## For Linux Users

### Ubuntu/Debian
1. `sudo apt install -y python3-pip && pip3 install ansible pexpect`
2. `ansible-playbook linux-setup.yml`
3. `ansible-playbook linux-aws-auth.yml`

## Troubleshooting

**Docker not working?**
- Ensure Docker Desktop is running
- Check: `docker version`

**WSL issues?**
- Check: `wsl --list --verbose`
- Restart: `wsl --shutdown && wsl`

**AWS auth failed?**
- Edit `config.yml` with correct SSO URL
- Run auth playbook again