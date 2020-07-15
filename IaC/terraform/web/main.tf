# ===========================
# AUTH
# ===========================
resource "aws_cognito_user_pool_client" "web" {
  name                                 = "${var.env}-${var.app}-web"
  user_pool_id                         = element(tolist(data.aws_cognito_user_pools.users.ids), 0)
  allowed_oauth_flows                  = ["code"]
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_scopes                 = ["aws.cognito.signin.user.admin", "email", "openid", "phone", "profile"]
  callback_urls                        = ["https://${data.aws_lb.public.dns_name}:4200"]
  explicit_auth_flows                  = ["ALLOW_ADMIN_USER_PASSWORD_AUTH", "ALLOW_CUSTOM_AUTH", "ALLOW_REFRESH_TOKEN_AUTH", "ALLOW_USER_PASSWORD_AUTH", "ALLOW_USER_SRP_AUTH"]
  logout_urls                          = ["https://${data.aws_lb.public.dns_name}:4200"]
  supported_identity_providers         = ["COGNITO"]
}

# resource "aws_cognito_identity_pool" "identity" {
#   identity_pool_name               = replace("${var.env}-${var.app}-identity-pool", "-", "_")
#   allow_unauthenticated_identities = false

#   cognito_identity_providers {
#     client_id               = aws_cognito_user_pool_client.web.id
#     provider_name           = "cognito-idp.${var.region}.amazonaws.com/${element(tolist(data.aws_cognito_user_pools.users.ids), 0)}"
#     server_side_token_check = false
#   }
# }

resource "aws_cognito_user_pool_domain" "web" {
  domain       = "${var.env}-${var.app}"
  user_pool_id = element(tolist(data.aws_cognito_user_pools.users.ids), 0)
}

# ===========================
# FARGATE
# ===========================
module "fargate" {
  source                           = "../modules/fargate"
  namespace                        = "${var.app}"
  stage                            = "${var.env}"
  name                             = "web"
  log_retention                    = 7
  iam_server_cert_arn              = data.aws_iam_server_certificate.self.arn
  container_port                   = 443
  vpc_id                           = data.aws_vpc.vpc.id
  health_check_interval            = 120
  health_check_unhealthy_threshold = 5
  health_check_healthy_threshold   = 3
  health_check_path                = "/"
  health_check_codes               = "307,202,200,404,302"
  load_balancer_arn                = data.aws_lb.public.arn
  load_balancer_port               = 4200
  container_image                  = "780016325729.dkr.ecr.us-east-1.amazonaws.com/con-pca-web:1.0"
  aws_region                       = var.region
  memory                           = 4096
  cpu                              = 2048
  container_protocol               = "HTTPS"

  environment = {
    "API_URL" : "CHANGEME",
    "FLOWER_URL" : "CHANGEME",
    "AWS_PROJECT_REGION" : var.region,
    "AWS_USER_POOLS_ID" : element(tolist(data.aws_cognito_user_pools.users.ids), 0),
    "AWS_USER_POOLS_WEB_CLIENT_ID" : aws_cognito_user_pool_client.web.id,
    "OAUTH_DOMAIN" : "${aws_cognito_user_pool_domain.web.domain}.auth.${var.region}.amazoncognito.com",
    "OAUTH_REDIRECT_URL" : "https://${data.aws_lb.public.dns_name}:4200",
    # "AWS_COGNITO_IDENTITY_POOL_ID" : aws_cognito_identity_pool.identity.id
  }

  desired_count      = 1
  subnet_ids         = data.aws_subnet_ids.public.ids
  security_group_ids = [aws_security_group.web.id]
}


# ===========================
# SECURITY GROUP
# ===========================
resource "aws_security_group" "web" {
  name        = "${var.app}-${var.env}-web-alb"
  description = "Allow traffic for web from alb"
  vpc_id      = data.aws_vpc.vpc.id

  ingress {
    description     = "Allow container port from ALB"
    from_port       = 443
    to_port         = 443
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
    "Name" = "${var.app}-${var.env}-gophish-alb"
  }

}
