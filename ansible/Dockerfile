FROM python:3.11-slim

WORKDIR /ansible

RUN apt-get update && apt-get install -y \
    curl \
    git \
    unzip \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install ansible pexpect boto3

# Install AWS CLI v2
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf awscliv2.zip aws

# Install Node.js LTS
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \
    && apt-get install -y nodejs

# Install AWS CDK
RUN npm install -g aws-cdk

COPY . .

CMD ["bash"]