# ===========================
# ROUTE 53
# ===========================
resource "aws_route53_record" "dev" {
  zone_id = data.aws_route53_zone.zone.zone_id
  name    = "${var.app}.dev.${data.aws_route53_zone.zone.name}"
  type    = "CNAME"
  ttl     = "300"
  records = [module.dev_alb.alb_dns_name]
}

# ===========================
# Certs
# ===========================
resource "aws_acm_certificate" "dev" {
  domain_name       = aws_route53_record.dev.name
  validation_method = "DNS"

  tags = {
    Environment = "dev"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "dev_validation" {
  for_each = {
    for dvo in aws_acm_certificate.dev.domain_validation_options : dvo.domain_name => {
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
  callback_urls                        = ["https://${module.dev_alb.alb_dns_name}", "https://${aws_route53_record.dev.name}"]
  explicit_auth_flows                  = ["ALLOW_ADMIN_USER_PASSWORD_AUTH", "ALLOW_CUSTOM_AUTH", "ALLOW_REFRESH_TOKEN_AUTH", "ALLOW_USER_PASSWORD_AUTH", "ALLOW_USER_SRP_AUTH"]
  logout_urls                          = ["https://${module.dev_alb.alb_dns_name}", "https://${aws_route53_record.dev.name}"]
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
