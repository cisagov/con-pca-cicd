# Locals
locals {
  api_container_port     = 5000
  landing_container_port = 8000
}

# Cloudwatch Logs
resource "aws_cloudwatch_log_group" "api" {
  name              = "${var.app}-${var.env}-api"
  retention_in_days = 7
}

# Container Definition
module "api_container" {
  source  = "cloudposse/ecs-container-definition/aws"
  version = "0.58.1"

  container_name  = "api"
  container_image = "${var.account_id}.dkr.ecr.${var.region}.amazonaws.com/${var.api_image_repo}:${var.api_image_tag}"
  essential       = true

  log_configuration = {
    logDriver = "awslogs"

    options = {
      awslogs-region        = var.region
      awslogs-group         = aws_cloudwatch_log_group.api.name
      awslogs-stream-prefix = "/ecs/${var.app}-${var.env}-api"
    }
  }

  port_mappings = [
    {
      containerPort = local.api_container_port
      hostPort      = local.api_container_port
      protocol      = "tcp"
    },
    {
      containerPort = local.landing_container_port
      hostPort      = local.landing_container_port
      protocol      = "tcp"
    }
  ]

  map_environment = {
    # AWS
    AWS_REGION         = var.region
    AWS_DEFAULT_REGION = var.region

    # Base Settings
    FLASK_APP   = "api.main:app"
    FLASK_DEBUG = 0
    WORKERS     = 6

    # Cognito
    AWS_COGNITO_ENABLED             = 1
    AWS_COGNITO_USER_POOL_ID        = aws_cognito_user_pool.pool.id
    AWS_COGNITO_USER_POOL_CLIENT_ID = aws_cognito_user_pool_client.client.id

    # Mailgun
    MAILGUN_API_KEY = var.mailgun_api_key

    # Maxmind
    MAXMIND_USER_ID     = var.maxmind_user_id
    MAXMIND_LICENSE_KEY = var.maxmind_license_key

    # Mongo
    MONGO_TYPE = "DOCUMENTDB"
    DB_HOST    = module.docdb.endpoint
    DB_PORT    = 27017
    DB_USER    = random_string.docdb_username.result
    DB_PW      = random_password.docdb_password.result

    # Redis Elasticache
    REDIS_HOST = module.redis.host
    REDIS_PORT = 6379

    # SES
    SES_ASSUME_ROLE_ARN = var.ses_arn
    SMTP_FROM           = var.reports_from_address

    # Tasks
    EMAIL_MINUTES = 5
    TASK_MINUTES  = 5
  }
}
