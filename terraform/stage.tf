# ===========================
# ROUTE 53
# ===========================
resource "aws_route53_record" "stage" {
  zone_id = data.aws_route53_zone.zone.zone_id
  name    = "${var.app}.stage.${data.aws_route53_zone.zone.name}"
  type    = "CNAME"
  ttl     = "300"
  records = [module.alb.alb_dns_name]
}

# ===========================
# Certs
# ===========================
resource "aws_acm_certificate" "stage" {
  domain_name       = aws_route53_record.stage.name
  validation_method = "DNS"

  tags = {
    Environment = "stage"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "stage_validation" {
  for_each = {
    for dvo in aws_acm_certificate.stage.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = data.aws_route53_zone.zone.zone_id
}

#=================================================
#  APPLICATION LOAD BALANCER
#=================================================
resource "aws_security_group" "alb" {
  name        = "${var.app}-stage-alb-sg"
  description = "Allowed ports into alb"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    "Name" = "${var.app}-stage-alb-sg"
  }
}

module "alb" {
  source             = "github.com/cloudposse/terraform-aws-alb"
  namespace          = "${var.app}"
  stage              = "stage"
  name               = "public"
  http_enabled       = false
  internal           = false
  vpc_id             = var.vpc_id
  security_group_ids = [aws_security_group.alb.id]
  subnet_ids         = var.public_subnet_ids
}

#=================================================
#  COGNITO
#=================================================
resource "aws_cognito_user_pool" "pool" {
  name = "${var.app}-stage-users"
}

resource "aws_cognito_user_pool_client" "client" {
  name                                 = "${var.app}-stage-client"
  user_pool_id                         = aws_cognito_user_pool.pool.id
  allowed_oauth_flows                  = ["code"]
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_scopes                 = ["aws.cognito.signin.user.admin", "email", "openid", "phone", "profile"]
  callback_urls                        = ["https://${module.alb.alb_dns_name}", "https://${aws_route53_record.stage.name}"]
  explicit_auth_flows                  = ["ALLOW_ADMIN_USER_PASSWORD_AUTH", "ALLOW_CUSTOM_AUTH", "ALLOW_REFRESH_TOKEN_AUTH", "ALLOW_USER_PASSWORD_AUTH", "ALLOW_USER_SRP_AUTH"]
  logout_urls                          = ["https://${module.alb.alb_dns_name}", "https://${aws_route53_record.stage.name}"]
  supported_identity_providers         = ["COGNITO"]
}

resource "aws_cognito_user_pool_domain" "domain" {
  domain       = "${var.app}-stage"
  user_pool_id = aws_cognito_user_pool.pool.id
}

resource "aws_ssm_parameter" "client_id" {
  name        = "/stage/${var.app}/cognito/client/id"
  description = "The client id for the client"
  type        = "SecureString"
  value       = aws_cognito_user_pool_client.client.id

  tags = {
    environment = "stage"
    app         = "${var.app}"
  }
}

resource "aws_ssm_parameter" "domain" {
  name        = "/stage/${var.app}/cognito/domain"
  description = "The domain for user pool"
  type        = "SecureString"
  value       = aws_cognito_user_pool_domain.domain.domain

  tags = {
    environment = "stage"
    app         = "${var.app}"
  }
}
