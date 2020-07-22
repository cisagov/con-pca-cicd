locals {
  browserless_port = 3000
  reports_port     = 3030

  environment = {
    "BROWSERLESS_ENDPOINT" : "pca-browserless:3000",
    "WEB_ENDPOINT" : "https://${data.aws_lb.public.dns_name}"
  }
}

module "browserless_container" {
  source    = "../modules/container-definition"
  namespace = var.app
  stage     = var.env
  name      = "browserless"

  container_name  = "pca-browserless"
  container_image = "browserless/chrome:latest"
  container_port  = local.browserless_port
  region          = var.region
  log_retention   = 7
  environment     = { "MAX_CONCURRENT_SESSIONS" : 10 }
}

module "reports_container" {
  source    = "../modules/container-definition"
  namespace = var.app
  stage     = var.env
  name      = "reports"

  container_name  = "pca-pdf-report"
  container_image = "${var.image_repo}:${var.image_tag}"
  container_port  = local.reports_port
  region          = var.region
  log_retention   = 7
  environment     = local.environment
}

module "fargate" {
  source    = "../modules/fargate"
  namespace = var.app
  stage     = var.env
  name      = "reports"

  iam_server_cert_arn              = data.aws_iam_server_certificate.self.arn
  container_port                   = local.reports_port
  container_definition             = "[${module.reports_container.json_map},${module.browserless_container.json_map}]"
  container_protocol               = "HTTP"
  container_name                   = "pca-pdf-report"
  memory                           = 2048
  cpu                              = 1024
  desired_count                    = 1
  vpc_id                           = data.aws_vpc.vpc.id
  health_check_interval            = 50
  health_check_unhealthy_threshold = 3
  health_check_healthy_threshold   = 3
  health_check_path                = "/"
  health_check_codes               = "200,202"
  load_balancer_arn                = data.aws_lb.private.arn
  load_balancer_port               = local.reports_port
  subnet_ids                       = data.aws_subnet_ids.private.ids
  security_group_ids               = [aws_security_group.reports.id]
}

resource "aws_security_group" "reports" {
  name        = "${var.app}-${var.env}-reports-alb"
  description = "Allow traffic for reports from alb"
  vpc_id      = data.aws_vpc.vpc.id

  ingress {
    description     = "Allow container port from ALB"
    from_port       = local.reports_port
    to_port         = local.reports_port
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
