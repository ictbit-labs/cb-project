#!/usr/bin/env python3
import os
import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_iam as iam,
    CfnOutput
)
from constructs import Construct

class IAMStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Get inputs from environment
        policy_name = os.environ.get('IAM_POLICY_NAME')
        role_name = os.environ.get('IAM_ROLE_NAME')
        bucket_name = os.environ.get('BUCKET_NAME')
        
        # Create IAM Policy first
        policy = iam.ManagedPolicy(
            self, "CustomPolicy",
            managed_policy_name=policy_name,
            statements=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=["s3:GetObject", "s3:PutObject"],
                    resources=[f"arn:aws:s3:::{bucket_name}/*"]
                )
            ]
        )

        # Create IAM Role that uses the policy
        role = iam.Role(
            self, "CustomRole",
            role_name=role_name,
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[policy]  # Attach the policy
        )

        # Outputs
        CfnOutput(self, "PolicyArn", value=policy.managed_policy_arn)
        CfnOutput(self, "RoleArn", value=role.role_arn)

app = cdk.App()

# Get configuration from environment variables
account = os.environ.get('CDK_DEFAULT_ACCOUNT')
region = os.environ.get('CDK_DEFAULT_REGION') or os.environ.get('CDK_REGION')
stack_name = os.environ.get('CDK_STACK_NAME', 'IAMStack')

IAMStack(app, stack_name, env=cdk.Environment(account=account, region=region))
app.synth()