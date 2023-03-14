resource "random_password" "tasks_api_key" {
  length  = 8
  numeric = true
  special = false
}

resource "aws_ssm_parameter" "tasks_api_key" {
  name        = "/${var.env}/${var.app}/tasks/api_key/master"
  description = "The api key for con-pca-tasks"
  type        = "SecureString"
  value       = random_password.tasks_api_key.result
}

# ===========================
# CLOUDWATCH LOGS
# ===========================
resource "aws_cloudwatch_log_group" "tasks" {
  name              = local.tasks_name
  retention_in_days = var.log_retention_days
}

# ===========================
# CONTAINER DEFINITION
# ===========================
module "tasks_container" {
  source  = "cloudposse/ecs-container-definition/aws"
  version = "0.58.1"

  container_name  = local.tasks_container_name
  container_image = "${var.account_id}.dkr.ecr.us-east-1.amazonaws.com/${var.tasks_image_repo}:${var.tasks_image_tag}"
  essential       = true

  log_configuration = {
    logDriver = "awslogs"
    options = {
      awslogs-region        = var.region
      awslogs-group         = aws_cloudwatch_log_group.tasks.name
      awslogs-stream-prefix = "/ecs/${local.tasks_container_name}"
    }
  }
  port_mappings = [
    {
      containerPort = local.tasks_container_port
      hostPort      = local.tasks_container_port
      protocol      = "tcp"
    }
  ]

  map_environment = {
    # API ACCESS KEY
    API_ACCESS_KEY = random_password.tasks_api_key.result

    # AWS
    AWS_DEFAULT_REGION = var.region

    # Con-PCA API URL
    API_URL = "https://${aws_route53_record.domain.name}"

    # MongoDB
    MONGO_CLUSTER_URI = replace(mongodbatlas_cluster.mongo-cluster.connection_strings[0].standard_srv, "mongodb+srv://", "mongodb+srv://${mongodbatlas_database_user.db-user.username}:${coalesce(nonsensitive(mongodbatlas_database_user.db-user.password), "null")}@")

    # SES
    SES_ASSUME_ROLE_ARN = var.ses_arn
    SMTP_FROM           = "pca-sandbox@cyber.dhs.gov"
  }
}
