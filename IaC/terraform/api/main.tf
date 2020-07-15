# ===========================
# DOCDB CREDS
# ===========================
resource "random_string" "docdb_username" {
  length  = 8
  number  = false
  special = false
  upper   = false
}

resource "aws_ssm_parameter" "docdb_username" {
  name        = "/${var.env}/${var.app}/api/docdb/username/master"
  description = "The username for document db"
  type        = "SecureString"
  value       = random_string.docdb_username.result

  tags = {
    environment = "${var.env}"
    app         = "${var.app}"
  }
}

resource "random_password" "docdb_password" {
  length           = 32
  special          = true
  override_special = "!_#&"
}

resource "aws_ssm_parameter" "docdb_password" {
  name        = "/${var.env}/${var.app}/api/docdb/password/master"
  description = "The password for document db"
  type        = "SecureString"
  value       = random_password.docdb_password.result

  tags = {
    environment = "${var.env}"
    app         = "${var.app}"
  }
}


# ===========================
# DOCUMENT DB
# ===========================
module "documentdb" {
  source                  = "github.com/cloudposse/terraform-aws-documentdb-cluster"
  stage                   = "${var.env}"
  name                    = "${var.env}-${var.app}-docdb"
  cluster_size            = 1
  master_username         = random_string.docdb_username.result
  master_password         = random_password.docdb_password.result
  instance_class          = "db.r5.large"
  vpc_id                  = data.aws_vpc.vpc.id
  subnet_ids              = data.aws_subnet_ids.public.ids
  allowed_cidr_blocks     = ["0.0.0.0/0"]
  allowed_security_groups = [aws_security_group.api.id]
  skip_final_snapshot     = true
}

# ===========================
# COGNITO
# ===========================
resource "aws_cognito_user_pool_client" "api" {
  name                                 = "${var.env}-${var.app}-api"
  user_pool_id                         = element(tolist(data.aws_cognito_user_pools.users.ids), 0)
  allowed_oauth_flows                  = ["code"]
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_scopes                 = ["aws.cognito.signin.user.admin", "email", "openid", "phone", "profile"]
  callback_urls                        = ["https://${data.aws_lb.public.dns_name}:4200"]
  explicit_auth_flows                  = ["ALLOW_ADMIN_USER_PASSWORD_AUTH", "ALLOW_CUSTOM_AUTH", "ALLOW_REFRESH_TOKEN_AUTH", "ALLOW_USER_PASSWORD_AUTH", "ALLOW_USER_SRP_AUTH"]
  logout_urls                          = ["https://${data.aws_lb.public.dns_name}:4200"]
  supported_identity_providers         = ["COGNITO"]
}


# ===========================
# APP CREDENTIALS
# ===========================
resource "random_string" "django_secret_key" {
  length  = 32
  number  = false
  special = false
  upper   = true
}

resource "random_string" "local_api_key" {
  length  = 32
  number  = false
  special = false
  upper   = true
}

resource "random_string" "basic_auth_username" {
  length  = 8
  number  = false
  special = false
  upper   = false
}

resource "random_password" "basic_auth_password" {
  length           = 32
  number           = true
  special          = false
  override_special = "!_#&"
}

# ===========================
# FARGATE
# ===========================
locals {
  api_container_port     = 80
  api_load_balancer_port = 8043

  environment = {
    "SECRET_KEY" : random_string.django_secret_key.result,
    "DEBUG" : 0,
    "DJANGO_ALLOWED_HOSTS" : "localhost 127.0.0.1 [::1] ${data.aws_lb.public.dns_name}",
    "CELERY_BROKER" : "CHANGEME",
    "BASIC_AUTH_USERNAME" : random_string.basic_auth_username.result,
    "BASIC_AUTH_PASSWORD" : random_password.basic_auth_password.result,
    "DB_HOST" : module.documentdb.endpoint,
    "DB_PORT" : 27017,
    "GP_URL" : "https://${data.aws_lb.public.dns_name}:3333/"
    "PHISH_URL" : "https://${data.aws_lb.public.dns_name}:8080/"
    "WEBHOOK_URL" : "https://${data.aws_lb.public.dns_name}:8043/api/v1/inboundwebhook/"
    "SMTP_FROM" : "postmaster@mg.inltesting.xyz",
    "AWS_S3_IMAGE_BUCKET" : "${var.app}-${var.env}-images",
    "DEFAULT_FILE_STORAGE" : "storages.backends.s3boto3.S3Boto3Storage",
    "WORKERS" : 4,
    "COGNITO_DEPLOYMENT_MODE" : "Production",
    "COGNITO_AWS_REGION" : var.region,
    "COGNITO_USER_POOL" : element(tolist(data.aws_cognito_user_pools.users.ids), 0),
    "COGNITO_AUDIENCE" : aws_cognito_user_pool_client.api.id,
    "LOCAL_API_KEY" : random_string.local_api_key.result
  }

  secrets = {
    "DB_USER" : aws_ssm_parameter.docdb_username.arn,
    "DB_PW" : aws_ssm_parameter.docdb_password.arn,
    "GP_API_KEY" : data.aws_ssm_parameter.gp_api_key.arn,
    "GP_SMTP_HOST" : data.aws_ssm_parameter.gp_smtp_host.arn,
    "GP_SMTP_FROM" : data.aws_ssm_parameter.gp_smtp_from.arn,
    "GP_SMTP_USER" : data.aws_ssm_parameter.gp_smtp_user.arn,
    "GP_SMTP_PASS" : data.aws_ssm_parameter.gp_smtp_pass.arn,
    "SMTP_HOST" : data.aws_ssm_parameter.smtp_host_no_port.arn,
    "SMTP_PORT" : data.aws_ssm_parameter.smtp_port.arn,
    "SMTP_PASS" : data.aws_ssm_parameter.gp_smtp_pass.arn
  }
}

module "fargate" {
  source                = "../modules/fargate"
  namespace             = "${var.app}"
  stage                 = "${var.env}"
  name                  = "api"
  log_retention         = 7
  iam_server_cert_arn   = data.aws_iam_server_certificate.self.arn
  container_port        = local.api_container_port
  vpc_id                = data.aws_vpc.vpc.id
  health_check_interval = 60
  health_check_path     = "/"
  health_check_codes    = "307,202,200,404"
  load_balancer_arn     = data.aws_lb.public.arn
  load_balancer_port    = local.api_load_balancer_port
  container_image       = "780016325729.dkr.ecr.us-east-1.amazonaws.com/con-pca-api:1.0"
  aws_region            = var.region
  cpu                   = 2048
  memory                = 4096
  environment           = local.environment
  secrets               = local.secrets
  desired_count         = 1
  subnet_ids            = data.aws_subnet_ids.public.ids
  security_group_ids    = [aws_security_group.api.id]
}

# ===========================
# SECURITY GROUP
# ===========================
resource "aws_security_group" "api" {
  name        = "${var.app}-${var.env}-api-alb"
  description = "Allow traffic for api from alb"
  vpc_id      = data.aws_vpc.vpc.id

  ingress {
    description     = "Allow container port from ALB"
    from_port       = local.api_container_port
    to_port         = local.api_container_port
    protocol        = "tcp"
    security_groups = [data.aws_security_group.alb.id]
    self            = true
  }

  egress {
    description = "Allow outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    "Name" = "${var.app}-${var.env}-api-alb"
  }

}
