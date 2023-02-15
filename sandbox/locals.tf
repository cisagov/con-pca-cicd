# ===========================
# LOCALS
# ===========================
locals {
  # API LOCALS
  api_name               = "${var.app}-${var.env}-api"
  api_container_name     = "${var.app}-api"
  api_container_port     = 5000
  api_container_protocol = "HTTP"

  # Landing Locals
  landing_container_port     = 8000
  landing_container_protocol = "HTTP"
  landing_name               = "${var.app}-${var.env}-landing"

  # Tasks Locals
  tasks_name               = "${var.app}-${var.env}-tasks"
  tasks_container_name     = "${var.app}-tasks"
  tasks_container_port     = 8080
  tasks_container_protocol = "HTTP"

  # UI LOCALS
  ui_container_port     = 80
  ui_container_name     = "ui"
  ui_container_protocol = "HTTP"
  ui_name               = "${var.app}-${var.env}-ui"

}
