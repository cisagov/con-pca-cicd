# Application Load Balancers
# This application needs two load balancers
#   1. An internal load balancer to serve the admin application and API
#   2. A public load balancer to serve the landing pages for tracking opens/clicks

# Internal Load Balancer
resource "aws_lb" "internal" {
  name               = "${var.app}-${var.env}-internal"
  idle_timeout       = 600
  internal           = true
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_internal.id]
  subnets            = local.private_subnet_ids

  enable_deletion_protection = true
}

# Public Load Balancer
resource "aws_lb" "public" {
  name               = "${var.app}-${var.env}-public-lb"
  idle_timeout       = 600
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_public.id]
  subnets            = local.public_subnet_ids

  enable_deletion_protection = true
}

# Internal Listener
resource "aws_lb_listener" "internal_https" {
  load_balancer_arn = aws_lb.internal.arn
  port              = 443
  protocol          = "HTTPS"
  certificate_arn   = module.internal_certs.acm_certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web.arn
  }
}

# Public Listener
resource "aws_lb_listener" "public_http" {
  load_balancer_arn = aws_lb.public.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.landing.arn
  }
}

