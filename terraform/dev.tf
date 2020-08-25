#=================================================
#  SELF-SIGNED CERTS
#=================================================
module "dev_certs" {
  source      = "./modules/certs"
  namespace   = var.app
  stage       = "dev"
  name        = "alb"
  dns_names   = [module.alb.alb_dns_name]
  common_name = module.alb.alb_dns_name
}

#=================================================
#  APPLICATION LOAD BALANCER
#=================================================
resource "aws_security_group" "dev_alb" {
  name        = "${var.app}-dev-alb-sg"
  description = "Allowed ports into alb"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    "Name" = "${var.app}-dev-alb-sg"
  }
}

module "dev_alb" {
  source             = "github.com/cloudposse/terraform-aws-alb"
  namespace          = "${var.app}"
  stage              = "dev"
  name               = "public"
  http_enabled       = false
  internal           = false
  vpc_id             = var.vpc_id
  security_group_ids = [aws_security_group.dev_alb.id]
  subnet_ids         = var.public_subnet_ids
}

module "dev_alb_internal" {
  source             = "github.com/cloudposse/terraform-aws-alb"
  namespace          = "${var.app}"
  stage              = "dev"
  name               = "private"
  http_enabled       = false
  internal           = true
  vpc_id             = var.vpc_id
  security_group_ids = [aws_security_group.dev_alb.id]
  subnet_ids         = var.private_subnet_ids
}

#=================================================
#  COGNITO
#=================================================
resource "aws_cognito_user_pool" "dev_pool" {
  name = "${var.app}-dev-users"
}

resource "aws_cognito_user_pool_client" "dev_client" {
  name                                 = "${var.app}-dev-client"
  user_pool_id                         = aws_cognito_user_pool.dev_pool.id
  allowed_oauth_flows                  = ["code"]
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_scopes                 = ["aws.cognito.signin.user.admin", "email", "openid", "phone", "profile"]
  callback_urls                        = ["https://${module.dev_alb.alb_dns_name}"]
  explicit_auth_flows                  = ["ALLOW_ADMIN_USER_PASSWORD_AUTH", "ALLOW_CUSTOM_AUTH", "ALLOW_REFRESH_TOKEN_AUTH", "ALLOW_USER_PASSWORD_AUTH", "ALLOW_USER_SRP_AUTH"]
  logout_urls                          = ["https://${module.dev_alb.alb_dns_name}"]
  supported_identity_providers         = ["COGNITO"]
}

resource "aws_cognito_user_pool_domain" "dev_domain" {
  domain       = "${var.app}-dev"
  user_pool_id = aws_cognito_user_pool.dev_pool.id
}

resource "aws_ssm_parameter" "dev_client_id" {
  name        = "/dev/${var.app}/cognito/client/id"
  description = "The client id for the client"
  type        = "SecureString"
  value       = aws_cognito_user_pool_client.dev_client.id
}

resource "aws_ssm_parameter" "dev_domain" {
  name        = "/dev/${var.app}/cognito/domain"
  description = "The domain for user pool"
  type        = "SecureString"
  value       = aws_cognito_user_pool_domain.dev_domain.domain
}
