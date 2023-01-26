# ===========================
# CLOUDWATCH LOGS
# ===========================
resource "aws_cloudwatch_log_group" "ui" {
  name              = local.ui_name
  retention_in_days = var.log_retention_days
}

# ===========================
# CONTAINER DEFINITION
# ===========================
module "ui_container" {
  source          = "github.com/cloudposse/terraform-aws-ecs-container-definition"
  container_name  = local.ui_container_name
  container_image = "${var.account_id}.dkr.ecr.us-east-1.amazonaws.com/${var.ui_image_repo}:${var.ui_image_tag}"
  essential       = "true"
  log_configuration = {
    logDriver = "awslogs"
    options = {
      awslogs-region        = var.region
      awslogs-group         = aws_cloudwatch_log_group.ui.name
      awslogs-stream-prefix = "/ecs/${local.ui_container_name}"
    }
  }
  port_mappings = [
    {
      containerPort = local.ui_container_port
      hostPort      = local.ui_container_port
      protocol      = "tcp"
    }
  ]

  map_environment = {
    API_URL       = "https://${aws_route53_record.domain.name}"
    ENVIRONMENT   = var.env
    UI_COMMIT_ID  = var.ui_image_tag
    DEPLOYED_DATE = var.deployed_date
  }
}
