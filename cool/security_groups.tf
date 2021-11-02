# Internal load balancer security group
resource "aws_security_group" "alb_internal" {
  name        = "${var.app}-${var.env}-alb-internal"
  description = "Allowed ports in internal load balancer"
  vpc_id      = local.vpc_id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/0"]
  }
}

# Public load balancer security group
resource "aws_security_group" "alb_public" {
  name        = "${var.app}-${var.env}-alb-public"
  description = "Allowed ports to public load balancer"
  vpc_id      = local.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ECS Service Security Group
resource "aws_security_group" "service" {
  name        = "${var.app}-${var.env}-service"
  description = "Allow traffic to ECS service from load balancers"
  vpc_id      = local.vpc_id

  ingress {
    description     = "Allow api container port from internal ALB"
    from_port       = local.api_container_port
    to_port         = local.api_container_port
    protocol        = "tcp"
    security_groups = [aws_security_group.alb_internal.id]
    self            = true
  }

  ingress {
    description     = "Allow web container port from internal ALB"
    from_port       = local.web_container_port
    to_port         = local.web_container_port
    protocol        = "tcp"
    security_groups = [aws_security_group.alb_internal.id]
    self            = true
  }

  ingress {
    description     = "Allow landing container port from public ALB"
    from_port       = local.landing_container_port
    to_port         = local.landing_container_port
    protocol        = "tcp"
    security_groups = [aws_security_group.alb_public.id]
    self            = true
  }

  egress {
    description = "Allow outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }
}
