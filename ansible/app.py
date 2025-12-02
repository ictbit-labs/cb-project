#!/usr/bin/env python3
import os
import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_s3 as s3,
    CfnOutput,
    RemovalPolicy
)
from constructs import Construct

class S3BucketStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Get configuration from environment variables
        bucket_base_name = os.environ.get('CDK_BUCKET_NAME', 'cb-project-bucket')
        
        # Create S3 bucket with unique name (lowercase only)
        bucket = s3.Bucket(
            self, "TestBucket",
            bucket_name=f"{bucket_base_name}-{self.account}-{self.region}".lower(),
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        # Output bucket name and ARN
        CfnOutput(
            self, "BucketName",
            value=bucket.bucket_name,
            description="S3 Bucket Name"
        )

        CfnOutput(
            self, "BucketArn", 
            value=bucket.bucket_arn,
            description="S3 Bucket ARN"
        )

app = cdk.App()

# Get configuration from environment variables
account = os.environ.get('CDK_DEFAULT_ACCOUNT')
region = os.environ.get('CDK_DEFAULT_REGION') or os.environ.get('CDK_REGION')
stack_name = os.environ.get('CDK_STACK_NAME', 'CBProjectStack')

S3BucketStack(app, stack_name, env=cdk.Environment(account=account, region=region))
app.synth()