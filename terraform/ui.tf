# ===========================
# ALB TARGET GROUP
# ===========================
resource "aws_lb_target_group" "ui" {
  name        = local.ui_name
  port        = local.ui_container_port
  protocol    = local.ui_container_protocol
  target_type = "ip"
  vpc_id      = var.vpc_id

  health_check {
    healthy_threshold   = 3
    interval            = 120
    matcher             = "202,200,307,404,302"
    path                = "/"
    port                = local.ui_container_port
    protocol            = local.ui_container_protocol
    unhealthy_threshold = 5
  }
}

#=========================
# ALB LISTENER RULE
#=========================
resource "aws_lb_listener_rule" "ui" {
  listener_arn = aws_lb_listener.https.arn
  priority     = 200

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.ui.arn
  }

  condition {
    path_pattern {
      values = ["/", "/*", "*"]
    }
  }
}

# ===========================
# CLOUDWATCH LOGS
# ===========================
resource "aws_cloudwatch_log_group" "ui" {
  name              = local.ui_name
  retention_in_days = var.log_retention_days
}

# ===========================
# CONTAINER DEFINITION
# ===========================
module "ui_container" {
  source          = "github.com/cloudposse/terraform-aws-ecs-container-definition"
  container_name  = local.ui_container_name
  container_image = "${var.account_id}.dkr.ecr.us-east-1.amazonaws.com/${var.ui_image_repo}:${var.ui_image_tag}"
  essential       = "true"
  log_configuration = {
    logDriver = "awslogs"
    options = {
      awslogs-region        = var.region
      awslogs-group         = aws_cloudwatch_log_group.ui.name
      awslogs-stream-prefix = "/ecs/${local.ui_container_name}"
    }
  }
  port_mappings = [
    {
      containerPort = local.ui_container_port
      hostPort      = local.ui_container_port
      protocol      = "tcp"
    }
  ]

  environment = [
    for key in keys(local.ui_environment) :
    {
      name  = key
      value = local.ui_environment[key]
    }
  ]
}

#=========================
# TASK DEFINITION
#=========================
resource "aws_ecs_task_definition" "ui" {
  family                   = local.ui_name
  container_definitions    = module.ui_container.json_map_encoded_list
  cpu                      = var.ui_cpu
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  memory                   = var.ui_memory
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  task_role_arn            = aws_iam_role.ecs_task.arn
}

#=========================
# SERVICE
#=========================
resource "aws_ecs_service" "ui" {
  name            = local.ui_container_name
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.ui.arn
  desired_count   = var.ui_desired_count
  launch_type     = "FARGATE"

  load_balancer {
    target_group_arn = aws_lb_target_group.ui.arn
    container_name   = local.ui_container_name
    container_port   = local.ui_container_port
  }

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.ui.id]
    assign_public_ip = false
  }
}

# ===========================
# SECURITY GROUP
# ===========================
resource "aws_security_group" "ui" {
  name        = "${local.ui_name}-alb"
  description = "Allow traffic for ui from alb"
  vpc_id      = var.vpc_id

  ingress {
    description     = "Allow container port from ALB"
    from_port       = local.ui_container_port
    to_port         = local.ui_container_port
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
    "Name" = "${local.ui_name}-alb"
  }
}
