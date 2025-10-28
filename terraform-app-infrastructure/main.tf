# main.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Provider configuration for multiple regions
provider "aws" {
  alias  = "eu_central"
  region = "eu-central-1"
}

provider "aws" {
  alias  = "china_beijing"
  region = "cn-north-1"
  # China region requires separate account and partnership
}

# EMEA VPC
module "vpc_emea" {
  source = "terraform-aws-modules/vpc/aws"
  providers = {
    aws = aws.eu_central
  }

  name = "app-emea-prod"
  cidr = "10.1.0.0/16"

  azs             = ["eu-central-1a", "eu-central-1b", "eu-central-1c"]
  private_subnets = ["10.1.1.0/24", "10.1.2.0/24", "10.1.3.0/24"]
  public_subnets  = ["10.1.101.0/24", "10.1.102.0/24", "10.1.103.0/24"]

  enable_nat_gateway = true
  enable_vpn_gateway = false

  tags = {
    Environment = "production"
    Region      = "emea"
    Compliance  = "gdpr"
  }
}

# Application Load Balancer with Geo-Routing
resource "aws_lb" "app_emea" {
  provider = aws.eu_central

  name               = "app-emea-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_emea.id]
  subnets            = module.vpc_emea.public_subnets

  enable_deletion_protection = true

  access_logs {
    bucket  = aws_s3_bucket.lb_logs.bucket
    prefix  = "emea-alb"
    enabled = true
  }

  tags = {
    Environment = "production"
  }
}

# ALB Listener with HTTPS termination
resource "aws_lb_listener" "app_https" {
  provider = aws.eu_central

  load_balancer_arn = aws_lb.app_emea.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = aws_acm_certificate.app.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}

# Auto Scaling Group
resource "aws_autoscaling_group" "app" {
  provider = aws.eu_central

  name_prefix          = "app-emea-"
  vpc_zone_identifier  = module.vpc_emea.private_subnets
  min_size            = 2
  max_size            = 10
  desired_capacity    = 3
  health_check_type   = "ELB"

  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }

  tag {
    key                 = "Environment"
    value               = "production"
    propagate_at_launch = true
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Scaling Policies
resource "aws_autoscaling_policy" "cpu_scaling" {
  provider = aws.eu_central

  name                   = "cpu-scaling-policy"
  autoscaling_group_name = aws_autoscaling_group.app.name
  policy_type           = "TargetTrackingScaling"

  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageCPUUtilization"
    }
    target_value = 70.0
  }
}