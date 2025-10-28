# compute.tf
resource "aws_launch_template" "app" {
  provider = aws.eu_central

  name_prefix   = "app-"
  image_id      = data.aws_ami.ubuntu.id
  instance_type = "t3.medium"
  key_name      = aws_key_pair.app.key_name

  vpc_security_group_ids = [aws_security_group.app_servers.id]

  user_data = base64encode(templatefile("${path.module}/user_data.sh", {
    app_version = var.app_version
    region      = "eu-central-1"
  }))

  iam_instance_profile {
    name = aws_iam_instance_profile.app.name
  }

  block_device_mappings {
    device_name = "/dev/sda1"

    ebs {
      volume_size = 20
      volume_type = "gp3"
      encrypted   = true
    }
  }

  monitoring {
    enabled = true
  }

  tag_specifications {
    resource_type = "instance"

    tags = {
      Name        = "app-server"
      Environment = "production"
    }
  }
}

# User data script for instance initialization
data "template_file" "user_data" {
  template = file("${path.module}/user_data.sh")

  vars = {
    app_version = var.app_version
    region      = "eu-central-1"
  }
}