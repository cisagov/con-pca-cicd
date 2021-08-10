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
  callback_urls                        = ["https://${module.alb.alb_dns_name}", "https://${aws_route53_record.domain.name}", "http://localhost:4200"]
  explicit_auth_flows                  = ["ALLOW_ADMIN_USER_PASSWORD_AUTH", "ALLOW_CUSTOM_AUTH", "ALLOW_REFRESH_TOKEN_AUTH", "ALLOW_USER_PASSWORD_AUTH", "ALLOW_USER_SRP_AUTH"]
  logout_urls                          = ["https://${module.alb.alb_dns_name}", "https://${aws_route53_record.domain.name}", "http://localhost:4200"]
  supported_identity_providers         = ["COGNITO"]
}

resource "aws_cognito_user_pool_domain" "domain" {
  domain       = "${var.app}-${var.env}"
  user_pool_id = aws_cognito_user_pool.pool.id
}
