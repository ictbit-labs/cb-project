@echo off
REM Quick launcher for Docker Ansible commands

if "%1"=="" (
    echo Usage: run-docker.bat [auth^|shell^|s3^|iam^|destroy^|playbook]
    echo   auth     - Run AWS SSO authentication
    echo   shell    - Open interactive shell
    echo   s3       - Deploy S3 bucket stack
    echo   iam      - Deploy IAM policy and role stack
    echo   destroy  - Destroy CDK resources
    echo   playbook - Run custom playbook ^(specify as second argument^)
    exit /b 1
)

if "%1"=="auth" (
    docker-compose run --rm ansible ansible-playbook docker-aws-auth.yml
) else if "%1"=="shell" (
    docker-compose run --rm ansible bash
) else if "%1"=="s3" (
    docker-compose run --rm ansible ansible-playbook cdk-simple.yml
) else if "%1"=="iam" (
    docker-compose run --rm ansible ansible-playbook iam-deploy.yml
) else if "%1"=="destroy" (
    docker-compose run --rm ansible ansible-playbook cdk-destroy.yml
) else if "%1"=="playbook" (
    if "%2"=="" (
        echo Please specify playbook name
        exit /b 1
    )
    docker-compose run --rm ansible ansible-playbook %2
) else (
    echo Unknown command: %1
    exit /b 1
)