
#=================================================
#  VPC and SUBNETS
#=================================================

module "vpc" {
  source     = "github.com/cloudposse/terraform-aws-vpc"
  namespace  = "${var.app}"
  stage      = "${var.env}"
  name       = "vpc"
  cidr_block = "10.0.0.0/16"
}

locals {
  public_cidr_block  = cidrsubnet(module.vpc.vpc_cidr_block, 1, 0)
  private_cidr_block = cidrsubnet(module.vpc.vpc_cidr_block, 1, 1)
}

module "subnets" {
  source              = "github.com/cloudposse/terraform-aws-dynamic-subnets"
  namespace           = var.app
  stage               = var.env
  name                = "subnet"
  vpc_id              = module.vpc.vpc_id
  igw_id              = module.vpc.igw_id
  cidr_block          = "10.0.0.0/16"
  availability_zones  = ["${var.region}a", "${var.region}b"]
  nat_gateway_enabled = true
}


#=================================================
#  S3
#=================================================
module "s3_images" {
  source        = "github.com/cloudposse/terraform-aws-s3-bucket"
  namespace     = "${var.app}"
  stage         = "${var.env}"
  name          = "images"
  acl           = "public-read"
  sse_algorithm = "AES256"
}

#=================================================
#  SELF-SIGNED CERTS
#=================================================
module "certs" {
  source      = "../modules/certs"
  namespace   = var.app
  stage       = var.env
  name        = "alb"
  dns_names   = [module.alb.alb_dns_name]
  common_name = module.alb.alb_dns_name
}

#=================================================
#  APPLICATION LOAD BALANCER
#=================================================
resource "aws_security_group" "alb" {
  name        = "${var.app}-${var.env}-alb-sg"
  description = "Allowed ports into alb"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    "Name" = "${var.app}-${var.env}-alb-sg"
  }
}

module "alb" {
  source             = "github.com/cloudposse/terraform-aws-alb"
  namespace          = "${var.app}"
  stage              = "${var.env}"
  name               = "public"
  http_enabled       = false
  internal           = false
  vpc_id             = module.vpc.vpc_id
  security_group_ids = [aws_security_group.alb.id]
  subnet_ids         = module.subnets.public_subnet_ids
}

#=================================================
#  COGNITO
#=================================================
resource "aws_cognito_user_pool" "pool" {
  name = "${var.app}-${var.env}-users"
}

resource "aws_cognito_user_pool_client" "client" {
  name                                 = "${var.app}-${var.env}-client"
  user_pool_id                         = aws_cognito_user_pool.pool.id
  allowed_oauth_flows                  = ["code"]
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_scopes                 = ["aws.cognito.signin.user.admin", "email", "openid", "phone", "profile"]
  callback_urls                        = ["https://${module.alb.alb_dns_name}"]
  explicit_auth_flows                  = ["ALLOW_ADMIN_USER_PASSWORD_AUTH", "ALLOW_CUSTOM_AUTH", "ALLOW_REFRESH_TOKEN_AUTH", "ALLOW_USER_PASSWORD_AUTH", "ALLOW_USER_SRP_AUTH"]
  logout_urls                          = ["https://${module.alb.alb_dns_name}"]
  supported_identity_providers         = ["COGNITO"]
}

resource "aws_cognito_user_pool_domain" "domain" {
  domain       = "${var.app}-${var.env}"
  user_pool_id = aws_cognito_user_pool.pool.id
}

resource "aws_ssm_parameter" "client_id" {
  name        = "/${var.env}/${var.app}/cognito/client/id"
  description = "The client id for the client"
  type        = "SecureString"
  value       = aws_cognito_user_pool_client.client.id

  tags = {
    environment = "${var.env}"
    app         = "${var.app}"
  }
}

resource "aws_ssm_parameter" "domain" {
  name        = "/${var.env}/${var.app}/cognito/domain"
  description = "The domain for user pool"
  type        = "SecureString"
  value       = aws_cognito_user_pool_domain.domain.domain

  tags = {
    environment = "${var.env}"
    app         = "${var.app}"
  }
}
