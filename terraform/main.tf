module "ansible_key" {
  source = "terraform-aws-modules/key-pair/aws"

  key_name           = "ansible-key"
  create_private_key = true
}

module "ansible_sg" {  
  source = "terraform-aws-modules/security-group/aws"
  name        = "ansible-sg"
  description = "Security group for ansible instances"
  vpc_id      = "vpc-0a4202d7eb54bf0ef"
  
  # Ingress rules with source security group ID
  ingress_with_cidr_blocks = [
    {
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      description = "Allow ssh access to ec2 instances"
      cidr_blocks = "0.0.0.0/0"
    }
  ]
  # Egress rules
  egress_with_cidr_blocks = [
    {
      from_port   = 0
      to_port     = 0
      protocol    = "-1"
      description = "Allow all outbound traffic"
      cidr_blocks = "0.0.0.0/0"
    }
  ]
  tags = {
    Name        = "ansible-sg"
    Project     = "Lab"
  }
}

locals {
  multiple_ec2_instances = {
    ansible1 = {
      subnet_id  = "subnet-0109b66439b968a1d"
      root_block_device = {
        encrypted  = true
        type       = "gp3"
        size       = 10
        delete_on_termination = true
      }
      volume_tags = {
        Name = "ansible1-volume"
      }
      ami = "ami-0ef32de3e8ab0640e"
      instance_type = "t3.micro"
      user_data = <<-EOT
      #!/bin/bash
      exec > >(tee /var/log/user-data-logs.log) 2>&1
      apt-get update
      apt-get install -y ca-certificates curl wget git unzip 2>&1
      EOT
    }
    # ansible2 = {
    #   subnet_id  = "subnet-0109b66439b968a1d"
    #   root_block_device = {
    #     encrypted  = true
    #     type       = "gp3"
    #     size       = 10
    #     delete_on_termination = true
    #   }
    #   volume_tags = {
    #     Name = "ansible2-volume"
    #   }
    #   ami = "ami-0ef32de3e8ab0640e"
    #   instance_type = "t3.micro"
    #   user_data = <<-EOT
    #   #!/bin/bash
    #   exec > >(tee /var/log/user-data-logs.log) 2>&1
    #   apt-get update
    #   apt-get install -y ca-certificates curl 2>&1
    #   EOT
    # }   
  }
}

# Disabled
module "ec2_instances" {
  source  = "terraform-aws-modules/ec2-instance/aws"
  for_each = local.multiple_ec2_instances
  name = "${each.key}-instance"
  instance_type = each.value.instance_type
  ami = each.value.ami
  create_spot_instance = true
  # spot_price           = "0.03"
  spot_type            = "persistent"
  spot_wait_for_fulfillment = true
  key_name      = module.ansible_key.key_pair_name

  monitoring    = true
  subnet_id         = each.value.subnet_id
  create_iam_instance_profile = false
  create_security_group = false
  vpc_security_group_ids = [module.ansible_sg.security_group_id]
  associate_public_ip_address = true
  user_data = each.value.user_data
  tags = {
    Name      = "-${each.key}-instance"
    Terraform   = true
    Project     = "Lab"
  }
  root_block_device = try(each.value.root_block_device, null)
  volume_tags = try(each.value.volume_tags, null)


  depends_on = [ module.ansible_key, module.ansible_sg]
}

output "ansible_private_key" {
  description = "EC2 private key"
  value       = module.ansible_key.private_key_pem
  sensitive   = true
}
output "ec2_public_ips" {
  description = "EC2 public IPs"
  value       = [for ec2 in module.ec2_instances : ec2.public_ip]
}

# Get the private key (works even with sensitive = true)
# terraform output -raw private_key > ec2-lab.pem
# chmod 400 ec2-lab.pem

# Alternative: Get from terraform state directly
# terraform show -json | jq -r '.values.outputs.private_key.value' > ec2-lab.pem
# chmod 400 ec2-lab.pem

# Get EC2 public IPs
# terraform output ec2_public_ips

# Connect to EC2
# ssh -i ec2-lab.pem admin@YOUR_EC2_PUBLIC_IP
