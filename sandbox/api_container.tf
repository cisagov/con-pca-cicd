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
    },
    {
      containerPort = local.landing_container_port
      hostPort      = local.landing_container_port
      protocol      = "tcp"
    }
  ]

  map_environment = {
    # Base Settings
    FLASK_APP   = "api.main:app"
    FLASK_DEBUG = 0
    WORKERS     = 6

    # Cognito
    AWS_COGNITO_ENABLED             = 1
    AWS_COGNITO_USER_POOL_ID        = aws_cognito_user_pool.pool.id
    AWS_COGNITO_USER_POOL_CLIENT_ID = aws_cognito_user_pool_client.client.id

    # Mongo
    MONGO_TYPE = "DOCUMENTDB"
    DB_HOST    = module.documentdb.endpoint
    DB_PORT    = 27017
    DB_USER    = aws_ssm_parameter.docdb_username.value
    DB_PW      = aws_ssm_parameter.docdb_password.value

    # Redis Elasticache
    REDIS_HOST = module.redis.endpoint
    REDIS_PORT = 6379

    # Report Email Address
    ARCHIVAL_EMAIL_ADDRESS = var.archival_email_address

    # SES
    SES_ASSUME_ROLE_ARN = var.ses_arn
    SMTP_FROM           = "pca-sandbox@cyber.dhs.gov"

    # Tasks
    EMAIL_MINUTES = 5
    TASK_MINUTES  = 5

    # Mailgun
    MAILGUN_API_KEY = var.mailgun_api_key

    # Maxmind
    MAXMIND_USER_ID     = var.maxmind_user_id
    MAXMIND_LICENSE_KEY = var.maxmind_license_key
  }

  environment = [
    for key in keys(local.api_environment) :
    {
      name  = key
      value = local.api_environment[key]
    }
  ]
}
