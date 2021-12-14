# Kubernetes: EKS with Fargate, ECR and a simple ALB, using Terraform & Helm

To execute (under CI/CD), use three automation scripts:

* [1-infrastructure-provisioning.sh](automation/1-infrastructure-provisioning.sh)
* [2-docker-build.sh](automation/2-docker-build.sh)
* [3-helm-deployment.sh](automation/3-helm-deployment.sh)

Source materials:

* [AWS Documentation: Creating a VPC for your Amazon EKS cluster](https://docs.aws.amazon.com/eks/latest/userguide/create-public-private-vpc.html)
* [AWS Documentation: CloudFormation template which the Terraform one is based on](https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/amazon-eks-vpc-sample.yaml)
* [Amazon EKS Workshop: Deploying Microservices to EKS Fargate](https://www.eksworkshop.com/beginner/180_fargate/)
* [AWS Documentation: Amazon EKS - Getting started with Fargate](https://docs.aws.amazon.com/eks/latest/userguide/fargate-getting-started.html)
* [AWS Documentation: AWS Fargate profile](https://docs.aws.amazon.com/eks/latest/userguide/fargate-profile.html)
* [AWS Documentation: Amazon EKS control plane logging](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html)
* [AWS Documentation: Fargate logging](https://docs.aws.amazon.com/eks/latest/userguide/fargate-logging.html)
* [AWS Documentation: Create an IAM OIDC provider for your cluster](https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html)
* [AWS Documentation: AWS Load Balancer Controller](https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html)
* [Kubernetes SIGs: Issue with Fargate profile for AWS Load Balancer Controller](https://github.com/kubernetes-sigs/aws-load-balancer-controller/issues/2261)
* [AWS Documentation: Application load balancing on Amazon EKS](https://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html)
* [AWS Documentation: Network load balancing on Amazon EKS (assigning Elastic IP to NLB)](https://docs.aws.amazon.com/eks/latest/userguide/network-load-balancing.html)
* [AWS Knowledge Center: How do I set up the AWS Load Balancer Controller on an Amazon EKS cluster for Fargate?](https://aws.amazon.com/premiumsupport/knowledge-center/eks-alb-ingress-controller-fargate/)
* [AWS Documentation: Example kubectl deployment YAML file](https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/examples/2048/2048_full.yaml)
* [AWS Documentation: Example kubectl deployment YAML file (newer syntax)](https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/examples/2048/2048_full_latest.yaml)
* [Kubernetes SIGs: Issue with ALB webhook CA verification](https://github.com/kubernetes-sigs/aws-load-balancer-controller/issues/2071)
* [Kubernetes SIGs: Issue with keepTLSSecret not honoured](https://github.com/kubernetes-sigs/aws-load-balancer-controller/issues/2312)
* [Rafay: Getting Started with Amazon EKS](https://rafay.co/the-kubernetes-current/getting-started-with-amazon-eks/)
* [AWS Documentation: Amazon EKS cluster endpoint access control](https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html)
* [AWS Knowledge Center: How do I set up an Application Load Balancer using the AWS Load Balancer Controller on an Amazon EC2 node group in Amazon EKS? (about cert manager)](https://aws.amazon.com/premiumsupport/knowledge-center/eks-alb-ingress-controller-setup/)
