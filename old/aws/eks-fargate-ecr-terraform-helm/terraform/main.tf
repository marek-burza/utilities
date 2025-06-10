terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = ">= 3.67.0"
    }
  }

  backend "s3" {
    bucket = "example-us-east-1-terraform-state"
    key = "example-service.tfstate"
    region = "us-east-1"
  }

  required_version = ">= 1.0.11"
}

provider "aws" {
  profile = "default"
}

locals {
  cluster_name = "examplecluster"
}

resource "aws_ecr_repository" "example-service" {
  name = "example-service"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }

  encryption_configuration {
    encryption_type = "AES256"
  }
}

resource "aws_iam_role" "examplerole" {
  name = "examplerole"

  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "eks.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  })

  managed_policy_arns = ["arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"]
}

# https://docs.aws.amazon.com/eks/latest/userguide/create-public-private-vpc.html
# https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/amazon-eks-vpc-sample.yaml

data "aws_availability_zones" "available" {
  state = "available"
}

resource "aws_vpc" "examplevpc" {
  cidr_block = "192.168.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true

  tags = {
    Name = "examplevpc"
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
  }
}

resource "aws_internet_gateway" "examplegateway" {
  vpc_id = aws_vpc.examplevpc.id
}

resource "aws_subnet" "examplepublicsubnet01" {
  map_public_ip_on_launch = true
  availability_zone = data.aws_availability_zones.available.names[0]
  cidr_block = "192.168.0.0/18"
  vpc_id = aws_vpc.examplevpc.id

  tags = {
    Name = "examplepublicsubnet01"
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
    "kubernetes.io/role/elb" = 1
  }
}

resource "aws_subnet" "examplepublicsubnet02" {
  map_public_ip_on_launch = true
  availability_zone = data.aws_availability_zones.available.names[1]
  cidr_block = "192.168.64.0/18"
  vpc_id = aws_vpc.examplevpc.id

  tags = {
    Name = "examplepublicsubnet02"
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
    "kubernetes.io/role/elb" = 1
  }
}

resource "aws_subnet" "exampleprivatesubnet01" {
  availability_zone = data.aws_availability_zones.available.names[0]
  cidr_block = "192.168.128.0/18"
  vpc_id = aws_vpc.examplevpc.id

  tags = {
    Name = "exampleprivatesubnet01"
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
    "kubernetes.io/role/internal-elb" = 1
  }
}

resource "aws_subnet" "exampleprivatesubnet02" {
  availability_zone = data.aws_availability_zones.available.names[1]
  cidr_block = "192.168.192.0/18"
  vpc_id = aws_vpc.examplevpc.id

  tags = {
    Name = "exampleprivatesubnet02"
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
    "kubernetes.io/role/internal-elb" = 1
  }
}

resource "aws_eip" "examplenatgateway01eip" {
  vpc = true

  depends_on = [aws_internet_gateway.examplegateway]
}

resource "aws_eip" "examplenatgateway02eip" {
  vpc = true

  depends_on = [aws_internet_gateway.examplegateway]
}

resource "aws_nat_gateway" "examplenatgateway01" {
  allocation_id = aws_eip.examplenatgateway01eip.id
  subnet_id = aws_subnet.examplepublicsubnet01.id

  tags = {
    Name = "examplenatgatewayaz1"
  }

  depends_on = [aws_eip.examplenatgateway01eip, aws_subnet.examplepublicsubnet01, aws_internet_gateway.examplegateway]
}

resource "aws_nat_gateway" "examplenatgateway02" {
  allocation_id = aws_eip.examplenatgateway02eip.id
  subnet_id = aws_subnet.examplepublicsubnet02.id

  tags = {
    Name = "examplenatgatewayaz2"
  }

  depends_on = [aws_eip.examplenatgateway02eip, aws_subnet.examplepublicsubnet02, aws_internet_gateway.examplegateway]
}

resource "aws_route_table" "examplepublicroutetable" {
  vpc_id = aws_vpc.examplevpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.examplegateway.id
  }

  tags = {
    Name = "Public Subnets"
    Network = "Public"
  }

  depends_on = [aws_internet_gateway.examplegateway]
}

resource "aws_route_table" "exampleprivateroutetable01" {
  vpc_id = aws_vpc.examplevpc.id

  route {
    cidr_block = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.examplenatgateway01.id
  }

  tags = {
    Name = "Private Subnet AZ1"
    Network = "Private01"
  }

  depends_on = [aws_internet_gateway.examplegateway, aws_nat_gateway.examplenatgateway01]
}

resource "aws_route_table" "exampleprivateroutetable02" {
  vpc_id = aws_vpc.examplevpc.id

  route {
    cidr_block = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.examplenatgateway02.id
  }

  tags = {
    Name = "Private Subnet AZ2"
    Network = "Private02"
  }

  depends_on = [aws_internet_gateway.examplegateway, aws_nat_gateway.examplenatgateway02]
}

resource "aws_route_table_association" "examplepublicsubnet01association" {
  subnet_id = aws_subnet.examplepublicsubnet01.id
  route_table_id = aws_route_table.examplepublicroutetable.id
}

resource "aws_route_table_association" "examplepublicsubnet02association" {
  subnet_id = aws_subnet.examplepublicsubnet02.id
  route_table_id = aws_route_table.examplepublicroutetable.id
}

resource "aws_route_table_association" "exampleprivatesubnet01association" {
  subnet_id = aws_subnet.exampleprivatesubnet01.id
  route_table_id = aws_route_table.exampleprivateroutetable01.id
}

resource "aws_route_table_association" "exampleprivatesubnet02association" {
  subnet_id = aws_subnet.exampleprivatesubnet02.id
  route_table_id = aws_route_table.exampleprivateroutetable02.id
}

resource "aws_security_group" "exampleclustersecuritygroup" {
  name = "exampleclustersecuritygroup"
  description = "Cluster communication with worker nodes"
  vpc_id = aws_vpc.examplevpc.id
}

# https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html

resource "aws_cloudwatch_log_group" "exampleloggroup" {
  name = "/aws/eks/${local.cluster_name}/cluster"
  retention_in_days = 7
}

resource "aws_eks_cluster" "examplecluster" {
  name = "${local.cluster_name}"
  role_arn = aws_iam_role.examplerole.arn
  version = "1.21"

  vpc_config {
    subnet_ids = [aws_subnet.examplepublicsubnet01.id, aws_subnet.examplepublicsubnet02.id, aws_subnet.examplepublicsubnet01.id, aws_subnet.examplepublicsubnet02.id]
    security_group_ids = [aws_security_group.exampleclustersecuritygroup.id]
  }

  enabled_cluster_log_types = ["api", "audit", "authenticator", "controllerManager", "scheduler"]

  depends_on = [aws_iam_role.examplerole, aws_cloudwatch_log_group.exampleloggroup]
}

# https://www.eksworkshop.com/beginner/180_fargate/
# https://docs.aws.amazon.com/eks/latest/userguide/fargate-getting-started.html
# https://docs.aws.amazon.com/eks/latest/userguide/fargate-profile.html

resource "aws_iam_role" "examplefargatepodexecutionrole" {
  name = "examplefargatepodexecutionrole"

  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "eks-fargate-pods.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "examplefargatepodexecutionrolepolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSFargatePodExecutionRolePolicy"
  role = aws_iam_role.examplefargatepodexecutionrole.name
}

resource "aws_eks_fargate_profile" "examplefargateprofile" {
  cluster_name = aws_eks_cluster.examplecluster.name
  fargate_profile_name = "examplefargateprofile"
  pod_execution_role_arn = aws_iam_role.examplefargatepodexecutionrole.arn
  subnet_ids = [aws_subnet.exampleprivatesubnet01.id, aws_subnet.exampleprivatesubnet02.id]

  selector {
    namespace = "examplefargatenamespace"
  }
}

resource "aws_eks_fargate_profile" "examplefargateprofilecoredns" {
  cluster_name = aws_eks_cluster.examplecluster.name
  fargate_profile_name = "coredns"
  pod_execution_role_arn = aws_iam_role.examplefargatepodexecutionrole.arn
  subnet_ids = [aws_subnet.exampleprivatesubnet01.id, aws_subnet.exampleprivatesubnet02.id]

  selector {
    namespace = "kube-system"
    labels = {
      "k8s-app" = "kube-dns"
    }
  }
}

# https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html

data "tls_certificate" "exampleclustercertificate" {
  url = aws_eks_cluster.examplecluster.identity[0].oidc[0].issuer

  depends_on = [aws_eks_cluster.examplecluster]
}

resource "aws_iam_openid_connect_provider" "exampleoidcprovider" {
  url = aws_eks_cluster.examplecluster.identity[0].oidc[0].issuer

  client_id_list = ["sts.amazonaws.com"]

  thumbprint_list = [data.tls_certificate.exampleclustercertificate.certificates[0].sha1_fingerprint]

  depends_on = [aws_eks_cluster.examplecluster]
}

# https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html
# https://github.com/kubernetes-sigs/aws-load-balancer-controller/issues/2261
# https://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html
# https://aws.amazon.com/premiumsupport/knowledge-center/eks-alb-ingress-controller-fargate/

resource "aws_eks_fargate_profile" "examplefargateprofileloadbalancer" {
  cluster_name = aws_eks_cluster.examplecluster.name
  fargate_profile_name = "awsalb"
  pod_execution_role_arn = aws_iam_role.examplefargatepodexecutionrole.arn
  subnet_ids = [aws_subnet.exampleprivatesubnet01.id, aws_subnet.exampleprivatesubnet02.id]

  selector {
    namespace = "kube-system"
    labels = {
      "app.kubernetes.io/name" = "aws-load-balancer-controller"
    }
  }
}

data "http" "exampleloadbalancerpolicycontent" {
  url = "https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.3.0/docs/install/iam_policy.json"
}

resource "aws_iam_policy" "exampleloadbalancerpolicy" {
  name = "exampleloadbalancerpolicy"
  policy =  data.http.exampleloadbalancerpolicycontent.body
}

data "aws_iam_policy_document" "exampleloadbalancerassumepolicy" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect = "Allow"

    condition {
      test = "StringEquals"
      variable = "${replace(aws_iam_openid_connect_provider.exampleoidcprovider.url, "https://", "")}:sub"
      values = ["system:serviceaccount:kube-system:aws-load-balancer-controller"]
    }

    principals {
      identifiers = [aws_iam_openid_connect_provider.exampleoidcprovider.arn]
      type = "Federated"
    }
  }
}

resource "aws_iam_role" "exampleloadbalancerrole" {
  name = "exampleloadbalancerrole"

  assume_role_policy = data.aws_iam_policy_document.exampleloadbalancerassumepolicy.json

  managed_policy_arns = [aws_iam_policy.exampleloadbalancerpolicy.arn]

  depends_on = [aws_iam_policy.exampleloadbalancerpolicy]
}

resource "local_file" "exampleloadbalancerserviceroleyaml" {
  filename = "aws-load-balancer-controller-service-account.yaml"
  content = yamlencode({
    "apiVersion": "v1",
    "kind": "ServiceAccount",
    "metadata": {
      "labels": {
        "app.kubernetes.io/component": "controller",
        "app.kubernetes.io/name": "aws-load-balancer-controller"
      },
      "name": "aws-load-balancer-controller",
      "namespace": "kube-system",
      "annotations": {
        "eks.amazonaws.com/role-arn": aws_iam_role.exampleloadbalancerrole.arn
      }
    }
  })

  depends_on = [aws_iam_role.exampleloadbalancerrole]
}

# https://docs.aws.amazon.com/eks/latest/userguide/fargate-logging.html

resource "aws_cloudwatch_log_group" "examplefargateloggroup" {
  name = "fluent-bit-cloudwatch"
  retention_in_days = 7
}

data "aws_region" "current" {}

resource "local_file" "examplefargateloggingconfigmapyaml" {
  filename = "aws-logging-cloudwatch-configmap.yaml"
  content = <<-EOT
    kind: ConfigMap
    apiVersion: v1
    metadata:
      name: aws-logging
      namespace: aws-observability
    data:
      output.conf: |
        [OUTPUT]
            Name cloudwatch_logs
            Match *
            region ${data.aws_region.current.name}
            log_group_name fluent-bit-cloudwatch
            log_stream_prefix from-fluent-bit-
            auto_create_group true
            log_key log
      parsers.conf: |
        [PARSER]
            Name crio
            Format Regex
            Regex ^(?<time>[^ ]+) (?<stream>stdout|stderr) (?<logtag>P|F) (?<log>.*)$
            Time_Key time
            Time_Format %Y-%m-%dT%H:%M:%S.%L%z
      filters.conf: |
        [FILTER]
            Name parser
            Match *
            Key_name log
            Parser crio
  EOT
}

data "http" "examplefargateloggingpolicycontent" {
  url = "https://raw.githubusercontent.com/aws-samples/amazon-eks-fluent-logging-examples/mainline/examples/fargate/cloudwatchlogs/permissions.json"
}

resource "aws_iam_policy" "examplefargateloggingpolicy" {
  name = "examplefargateloggingpolicy"
  policy =  data.http.examplefargateloggingpolicycontent.body
}

resource "aws_iam_role_policy_attachment" "examplefargatepodexecutionfargateloggingpolicy" {
  policy_arn = aws_iam_policy.examplefargateloggingpolicy.arn
  role = aws_iam_role.examplefargatepodexecutionrole.name
}
