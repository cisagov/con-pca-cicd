# Locals 
locals {
  web_container_port = 80
}

# Cloudwatch Logs
resource "aws_cloudwatch_log_group" "web" {
  name              = "${var.app}-${var.env}-web"
  retention_in_days = 7
}

# Container Definition
module "web_container" {
  source  = "cloudposse/ecs-container-definition/aws"
  version = "0.58.1"

  container_name  = "web"
  container_image = "${var.account_id}.dkr.ecr.${var.region}.amazonaws.com/${var.web_image_repo}:${var.web_image_tag}"
  essential       = true

  log_configuration = {
    logDriver = "awslogs"

    options = {
      awslogs-region        = var.region
      awslogs-group         = aws_cloudwatch_log_group.web.name
      awslogs-stream-prefix = "/ecs/${var.app}-${var.env}-web"
    }
  }

  port_mappings = [
    {
      containerPort = local.web_container_port
      hostPort      = local.web_container_port
      protocol      = "tcp"
    },
  ]

  map_environment = {
    API_URL       = "https://${aws_route53_record.sharedservices_internal_web.name}"
    DEPLOYED_DATE = var.deployed_date
  }
}
