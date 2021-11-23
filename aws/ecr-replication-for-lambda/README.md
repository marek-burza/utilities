# Cross-region (cross-account) ECR replication for AWS Lambda

Currently Lambda restricts access to ECR to the same region as the Lambda function (see: [here](https://aws.amazon.com/blogs/compute/introducing-cross-account-amazon-ecr-access-for-aws-lambda/)) even though it allows an access to an ECR from another account.

To resolve this, use ECR replication to different regions (or even different account and regions) - see more about this [here](https://aws.amazon.com/blogs/containers/cross-region-replication-in-amazon-ecr-has-landed/). Please mind that for a cross-account ECR replication an additional policy is required - see: [here](https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry-permissions-create.html).

Note: There is however an open issue regarding the resriction [here](https://github.com/aws/containers-roadmap/issues/1281).
