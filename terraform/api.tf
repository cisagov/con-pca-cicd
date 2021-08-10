# ===========================
# APP CREDENTIALS
# ===========================
resource "random_password" "api_key" {
  length  = 32
  number  = false
  special = false
  upper   = true
}

resource "aws_ssm_parameter" "api_key" {
  name        = "/${var.env}/${var.app}/api/key"
  description = "api key for ${var.app}"
  type        = "SecureString"
  value       = random_password.api_key.result
}

# ===========================
# CLOUDWATCH LOGS
# ===========================
resource "aws_cloudwatch_log_group" "api" {
  name              = local.api_name
  retention_in_days = var.log_retention_days
}

# ===========================
# ALB TARGET GROUPS
# ===========================
resource "aws_lb_target_group" "api" {
  name        = local.api_name
  port        = local.api_container_port
  protocol    = local.api_container_protocol
  target_type = "ip"
  vpc_id      = var.vpc_id

  health_check {
    healthy_threshold   = 3
    interval            = 60
    matcher             = "200"
    path                = "/"
    port                = local.api_container_port
    protocol            = local.api_container_protocol
    unhealthy_threshold = 3
  }
}

#=========================
# ALB LISTENER RULE
#=========================
resource "aws_lb_listener_rule" "api" {
  listener_arn = aws_lb_listener.https.arn
  priority     = 100

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.api.arn
  }

  condition {
    path_pattern {
      values = ["/api/*", "/api/", "/api"]
    }
  }
}

# ===========================
# CONTAINER DEFINITION
# ===========================
module "api_container" {
  source          = "github.com/cloudposse/terraform-aws-ecs-container-definition"
  container_name  = local.api_container_name
  container_image = "${var.account_id}.dkr.ecr.us-east-1.amazonaws.com/${var.api_image_repo}:${var.api_image_tag}"
  essential       = "true"
  log_configuration = {
    logDriver = "awslogs"
    options = {
      awslogs-region        = var.region
      awslogs-group         = aws_cloudwatch_log_group.api.name
      awslogs-stream-prefix = "/ecs/${local.api_container_name}"
    }
  }
  port_mappings = [
    {
      containerPort = local.api_container_port
      hostPort      = local.api_container_port
      protocol      = "tcp"
    }
  ]

  environment = [
    for key in keys(local.api_environment) :
    {
      name  = key
      value = local.api_environment[key]
    }
  ]
}

#=========================
# TASK DEFINITION
#=========================
resource "aws_ecs_task_definition" "api" {
  family                   = local.api_name
  container_definitions    = module.api_container.json_map_encoded_list
  cpu                      = var.api_cpu
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  memory                   = var.api_memory
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  task_role_arn            = aws_iam_role.ecs_task.arn
}

#=========================
# SERVICE
#=========================
resource "aws_ecs_service" "api" {
  name            = local.api_container_name
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.api.arn
  desired_count   = var.api_desired_count
  launch_type     = "FARGATE"

  load_balancer {
    target_group_arn = aws_lb_target_group.api.arn
    container_name   = local.api_container_name
    container_port   = local.api_container_port
  }

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.api.id]
    assign_public_ip = false
  }

  lifecycle {
    ignore_changes = [desired_count]
  }
}

# ===========================
# SECURITY GROUP
# ===========================
resource "aws_security_group" "api" {
  name        = "${local.api_name}-alb"
  description = "Allow traffic for api from alb"
  vpc_id      = var.vpc_id

  ingress {
    description     = "Allow container port from ALB"
    from_port       = local.api_container_port
    to_port         = local.api_container_port
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
    "Name" = "${local.api_name}-alb"
  }
}
