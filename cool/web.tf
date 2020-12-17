# ===========================
# LOCALS
# ===========================

locals {
  web_container_port     = 80
  web_container_name     = "web"
  web_container_protocol = "HTTP"
  web_load_balancer_port = 443
  web_name               = "${var.app}-${var.env}-web"

  web_environment = {
    "API_URL" : "https://${aws_route53_record.internal.name}:${local.api_load_balancer_port}"
    "API_URL_HEADLESS" : "https://${aws_route53_record.internal.name}:${local.api_load_balancer_port}"
    "AWS_PROJECT_REGION" : var.region
    "AWS_USER_POOLS_ID" : aws_cognito_user_pool.pool.id
    "OAUTH_DOMAIN" : "${aws_cognito_user_pool_domain.domain.domain}.auth.${var.region}.amazoncognito.com"
    "OAUTH_REDIRECT_URL" : "https://${aws_route53_record.internal.name}"
    "AWS_USER_POOLS_WEB_CLIENT_ID" : aws_cognito_user_pool_client.client.id
  }
}

# ===========================
# ALB TARGET GROUP
# ===========================
resource "aws_lb_target_group" "web" {
  name        = local.web_name
  port        = local.web_container_port
  protocol    = local.web_container_protocol
  target_type = "ip"
  vpc_id      = local.vpc_id

  health_check {
    healthy_threshold   = 3
    interval            = 120
    matcher             = "202,200,307,404,302"
    path                = "/"
    port                = local.web_container_port
    protocol            = local.web_container_protocol
    unhealthy_threshold = 5
  }
}

#=========================
# ALB LISTENER
#=========================
resource "aws_lb_listener" "web" {
  load_balancer_arn = module.internal_alb.alb_arn
  port              = local.web_load_balancer_port
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = module.internal_certs.this_acm_certificate_arn

  default_action {
    target_group_arn = aws_lb_target_group.web.arn
    type             = "forward"
  }
}

# ===========================
# CLOUDWATCH LOGS
# ===========================
resource "aws_cloudwatch_log_group" "web" {
  name              = local.web_name
  retention_in_days = var.log_retention_days
}

# ===========================
# CONTAINER DEFINITION
# ===========================
module "web_container" {
  source          = "github.com/cloudposse/terraform-aws-ecs-container-definition"
  container_name  = local.web_container_name
  container_image = "${var.image_url}/${var.web_image_repo}:${var.web_image_tag}"
  essential       = "true"
  log_configuration = {
    logDriver = "awslogs"
    options = {
      awslogs-region        = var.region
      awslogs-group         = aws_cloudwatch_log_group.web.name
      awslogs-stream-prefix = "/ecs/${local.web_container_name}"
    }
  }
  port_mappings = [
    {
      containerPort = local.web_container_port
      hostPort      = local.web_container_port
      protocol      = "tcp"
    }
  ]

  environment = [
    for key in keys(local.web_environment) :
    {
      name  = key
      value = local.web_environment[key]
    }
  ]
}

#=========================
# TASK DEFINITION
#=========================
resource "aws_ecs_task_definition" "web" {
  family                   = local.web_name
  container_definitions    = module.web_container.json_map_encoded_list
  cpu                      = var.web_cpu
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  memory                   = var.web_memory
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  task_role_arn            = aws_iam_role.ecs_task.arn
}

#=========================
# SERVICE
#=========================
resource "aws_ecs_service" "web" {
  name            = local.web_container_name
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.web.arn
  desired_count   = var.web_desired_count
  launch_type     = "FARGATE"

  load_balancer {
    target_group_arn = aws_lb_target_group.web.arn
    container_name   = local.web_container_name
    container_port   = local.web_container_port
  }

  network_configuration {
    subnets          = local.private_subnet_ids
    security_groups  = [aws_security_group.web.id]
    assign_public_ip = false
  }
}

# ===========================
# SECURITY GROUP
# ===========================
resource "aws_security_group" "web" {
  name        = "${local.web_name}-alb"
  description = "Allow traffic for web from alb"
  vpc_id      = local.vpc_id

  ingress {
    description     = "Allow container port from ALB"
    from_port       = local.web_container_port
    to_port         = local.web_container_port
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
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
    "Name" = "${local.web_name}-alb"
  }

}
