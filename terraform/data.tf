
# ===========================
# ROUTE 53
# ===========================
data "aws_route53_zone" "zone" {
  name = var.route53_zone_name
}

# ===========================
# SSM
# ===========================
data "aws_ssm_parameter" "gp_api_key" {
  name = "/${var.env}/${var.app}/gophish/apikey"
}

data "aws_ssm_parameter" "gp_smtp_host" {
  name = "/${var.env}/${var.app}/mailgun/gp_smtp_host"
}

data "aws_ssm_parameter" "gp_smtp_from" {
  name = "/${var.env}/${var.app}/mailgun/gp_smtp_from"
}

data "aws_ssm_parameter" "gp_smtp_pass" {
  name = "/${var.env}/${var.app}/mailgun/gp_smtp_pass"
}

data "aws_ssm_parameter" "gp_smtp_user" {
  name = "/${var.env}/${var.app}/mailgun/gp_smtp_user"
}

data "aws_ssm_parameter" "smtp_from" {
  name = "/${var.env}/${var.app}/ses/smtp_from"
}

data "aws_ssm_parameter" "smtp_host" {
  name = "/${var.env}/${var.app}/mailgun/smtp_host"
}

data "aws_ssm_parameter" "smtp_pass" {
  name = "/${var.env}/${var.app}/mailgun/smtp_pass"
}

data "aws_ssm_parameter" "smtp_port" {
  name = "/${var.env}/${var.app}/mailgun/smtp_port"
}

data "aws_ssm_parameter" "smtp_user" {
  name = "/${var.env}/${var.app}/mailgun/smtp_user"
}

data "aws_ssm_parameter" "ses_assume_role_arn" {
  name = "/${var.env}/${var.app}/ses/assume_role_arn"
}
