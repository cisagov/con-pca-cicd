resource "aws_ssm_parameter" "maxmind_user_id" {
  name        = "/${var.env}/${var.app}/maxmind/userid"
  description = "The user id for maxmind"
  type        = "SecureString"
  value       = "get_from_maxmind"

  lifecycle {
    ignore_changes = [value]
  }
}

resource "aws_ssm_parameter" "maxmind_license_key" {
  name        = "/${var.env}/${var.app}/maxmind/licensekey"
  description = "The license key for maxmind"
  type        = "SecureString"
  value       = "get_from_maxmind"

  lifecycle {
    ignore_changes = [value]
  }
}
