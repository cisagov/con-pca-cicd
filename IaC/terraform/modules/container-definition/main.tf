module "label" {
  source     = "github.com/cloudposse/terraform-null-label"
  enabled    = true
  attributes = []
  delimiter  = "-"
  name       = var.name
  namespace  = var.namespace
  stage      = var.stage
  tags       = {}
}

resource "aws_cloudwatch_log_group" "_" {
  name              = module.label.id
  retention_in_days = var.log_retention
}

module "container" {
  source          = "github.com/cloudposse/terraform-aws-ecs-container-definition"
  container_name  = var.container_name
  container_image = var.container_image
  entrypoint      = var.entrypoint
  essential       = "true"
  log_configuration = {
    logDriver = "awslogs"
    options = {
      awslogs-region        = var.region
      awslogs-group         = aws_cloudwatch_log_group._.name
      awslogs-stream-prefix = "/ecs/${var.name}"
    }
  }
  port_mappings = [
    {
      containerPort = var.container_port
      hostPort      = var.container_port
      protocol      = "tcp"
    }
  ]

  environment = [
    for key in keys(var.environment) :
    {
      name  = key
      value = var.environment[key]
    }
  ]

  secrets = [
    for key in keys(var.secrets) :
    {
      name      = key
      valueFrom = var.secrets[key]
    }
  ]
}
