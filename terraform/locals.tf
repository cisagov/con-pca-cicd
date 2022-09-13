# ===========================
# LOCALS
# ===========================
locals {
  # API LOCALS
  api_name               = "${var.app}-${var.env}-api"
  api_container_name     = "${var.app}-api"
  api_container_port     = 5000
  api_container_protocol = "HTTP"

  api_environment = {
    "FLASK_APP" : "main"
    "FLASK_DEBUG" : 0
    "DB_PW" : aws_ssm_parameter.docdb_password.value
    "DB_USER" : aws_ssm_parameter.docdb_username.value
    "DB_HOST" : module.documentdb.endpoint
    "DB_PORT" : 27017
    "MONGO_TYPE" : "DOCUMENTDB"
    "WORKERS" : 6
    "AWS_COGNITO_ENABLED" : 1
    "AWS_COGNITO_USER_POOL_ID" : aws_cognito_user_pool.pool.id
    "AWS_COGNITO_USER_POOL_CLIENT_ID" : aws_cognito_user_pool_client.client.id
    "SES_ASSUME_ROLE_ARN" : var.ses_arn
    "SMTP_FROM" : "pca-sandbox@cyber.dhs.gov"
    "DEPLOYED_DATE" : var.deployed_date
    "API_COMMIT_ID" : var.api_image_tag
    "UI_COMMIT_ID" : var.ui_image_tag
    "AWS_REGION" : var.region
    "AWS_DEFAULT_REGION" : var.region
    "LANDING_SUBDOMAIN" : var.landing_subdomain
    "MAXMIND_USER_ID" : var.maxmind_user_id
    "MAXMIND_LICENSE_KEY" : var.maxmind_license_key
  }

  # Landing Locals
  landing_container_port     = 8000
  landing_container_protocol = "HTTP"
  landing_name               = "${var.app}-${var.env}-landing"

  # UI LOCALS
  ui_container_port     = 80
  ui_container_name     = "ui"
  ui_container_protocol = "HTTP"
  ui_name               = "${var.app}-${var.env}-ui"

  ui_environment = {
    "API_URL" : "https://${aws_route53_record.domain.name}"
    "DEPLOYED_DATE" : var.deployed_date
    "UI_COMMIT_ID" : var.ui_image_tag
  }
}
