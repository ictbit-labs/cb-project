provider "aws" {
  region = "eu-central-1"
}
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
  backend "s3" {
    bucket = var.bucket_name
    key    = "terraform-state/eu-central-1/ansible"
    region = "eu-central-1"
  }  
}