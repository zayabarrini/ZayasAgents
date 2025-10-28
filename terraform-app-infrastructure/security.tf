# security.tf
resource "aws_security_group" "alb_emea" {
  provider = aws.eu_central

  name        = "alb-emea-sg"
  description = "ALB security group for EMEA"
  vpc_id      = module.vpc_emea.vpc_id

  # HTTP/HTTPS from anywhere
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTP traffic"
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS traffic"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "alb-emea-sg"
  }
}

resource "aws_security_group" "app_servers" {
  provider = aws.eu_central

  name        = "app-servers-sg"
  description = "Application servers security group"
  vpc_id      = module.vpc_emea.vpc_id

  # Allow traffic only from ALB
  ingress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.alb_emea.id]
    description     = "App traffic from ALB"
  }

  # DNS resolution
  egress {
    from_port   = 53
    to_port     = 53
    protocol    = "udp"
    cidr_blocks = ["10.1.0.0/16"]
    description = "DNS queries to VPC resolver"
  }

  # Outbound HTTPS for external APIs
  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS to external services"
  }

  tags = {
    Name = "app-servers-sg"
  }
}