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
    "DEPLOYED_DATE" : var.deployed_date
    "API_COMMIT_ID" : var.api_image_tag
    "UI_COMMIT_ID" : var.ui_image_tag
    "AWS_REGION" : var.region
    "AWS_DEFAULT_REGION" : var.region
    "LANDING_SUBDOMAIN" : var.landing_subdomain
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
