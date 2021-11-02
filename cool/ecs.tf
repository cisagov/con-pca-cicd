# ECS Cluster
resource "aws_ecs_cluster" "cluster" {
  name = "${var.app}-${var.env}"
}

# Task Definition
resource "aws_ecs_task_definition" "task" {
  family = "${var.app}-${var.env}"

  container_definitions = jsonencode([
    module.api_container.json_map_object,
    module.web_container.json_map_object
  ])

  cpu                      = var.cpu
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  memory                   = var.memory
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  task_role_arn            = aws_iam_role.ecs_task.arn
}

# Service
resource "aws_ecs_service" "service" {
  name            = "${var.app}-${var.env}"
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.task.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  load_balancer {
    target_group_arn = aws_lb_target_group.api.arn
    container_name   = "api"
    container_port   = local.api_container_port

  }

  load_balancer {
    target_group_arn = aws_lb_target_group.web.arn
    container_name   = "web"
    container_port   = local.web_container_port
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.landing.arn
    container_name   = "api"
    container_port   = local.landing_container_port
  }

  network_configuration {
    subnets          = local.private_subnet_ids
    security_groups  = [aws_security_group.service.id]
    assign_public_ip = false
  }

  lifecycle {
    ignore_changes = [desired_count]
  }
}
