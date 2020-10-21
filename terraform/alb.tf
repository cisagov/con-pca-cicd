#=================================================
#  APPLICATION LOAD BALANCER
#=================================================
resource "aws_security_group" "alb" {
  name        = "${var.app}-${var.env}-alb-sg"
  description = "Allowed ports into alb"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    "Name" = "${var.app}-${var.env}-alb-sg"
  }
}

module "public_alb" {
  source             = "github.com/cloudposse/terraform-aws-alb"
  namespace          = var.app
  stage              = var.env
  name               = "public"
  http_enabled       = false
  idle_timeout       = var.idle_timeout
  internal           = false
  vpc_id             = var.vpc_id
  security_group_ids = [aws_security_group.alb.id]
  subnet_ids         = var.public_subnet_ids
}

module "internal_alb" {
  source             = "github.com/cloudposse/terraform-aws-alb"
  namespace          = var.app
  stage              = var.env
  name               = "internal"
  http_enabled       = false
  idle_timeout       = var.idle_timeout
  internal           = true
  vpc_id             = var.vpc_id
  security_group_ids = [aws_security_group.alb.id]
  subnet_ids         = var.public_subnet_ids
}

#=================================================
#  NETWORK LOAD BALANCER
#=================================================
resource "aws_lb" "network" {
  name                             = "${var.app}-${var.env}-network"
  enable_cross_zone_load_balancing = true
  idle_timeout                     = 60
  internal                         = true
  load_balancer_type               = "network"
  subnets                          = var.private_subnet_ids
}
