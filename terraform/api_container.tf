# ===========================
# CLOUDWATCH LOGS
# ===========================
resource "aws_cloudwatch_log_group" "api" {
  name              = local.api_name
  retention_in_days = var.log_retention_days
}

# ===========================
# CONTAINER DEFINITION
# ===========================
module "api_container" {
  source          = "github.com/cloudposse/terraform-aws-ecs-container-definition"
  container_name  = local.api_container_name
  container_image = "${var.account_id}.dkr.ecr.us-east-1.amazonaws.com/${var.api_image_repo}:${var.api_image_tag}"
  essential       = "true"
  log_configuration = {
    logDriver = "awslogs"
    options = {
      awslogs-region        = var.region
      awslogs-group         = aws_cloudwatch_log_group.api.name
      awslogs-stream-prefix = "/ecs/${local.api_container_name}"
    }
  }
  port_mappings = [
    {
      containerPort = local.api_container_port
      hostPort      = local.api_container_port
      protocol      = "tcp"
    }
  ]

  environment = [
    for key in keys(local.api_environment) :
    {
      name  = key
      value = local.api_environment[key]
    }
  ]
}
