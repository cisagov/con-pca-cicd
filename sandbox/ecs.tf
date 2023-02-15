# ===========================
# CLUSTER
# ===========================
resource "aws_ecs_cluster" "cluster" {
  name = "${var.app}-${var.env}"
}

#=========================
# TASK DEFINITION
#=========================
resource "aws_ecs_task_definition" "task" {
  family = "${var.app}-${var.env}"

  container_definitions = jsonencode([
    module.ui_container.json_map_object,
    module.api_container.json_map_object,
    module.tasks_container.json_map_object,
  ])

  cpu                      = var.cpu
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  memory                   = var.memory
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  task_role_arn            = aws_iam_role.ecs_task.arn
}

# ===========================
# SECURITY GROUP
# ===========================
resource "aws_security_group" "service" {
  name        = "${var.app}-${var.env}-service"
  description = "Allow traffic to service from ALB"
  vpc_id      = var.vpc_id

  ingress {
    description     = "Allow container port from ALB"
    from_port       = local.api_container_port
    to_port         = local.api_container_port
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
    self            = true
  }

  ingress {
    description     = "Allow container port from ALB"
    from_port       = local.ui_container_port
    to_port         = local.ui_container_port
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
    self            = true
  }

  ingress {
    description     = "Allow traffic to containers"
    from_port       = local.landing_container_port
    to_port         = local.landing_container_port
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
}


#=========================
# SERVICE
#=========================
resource "aws_ecs_service" "service" {
  name                 = "${var.app}-${var.env}"
  cluster              = aws_ecs_cluster.cluster.id
  task_definition      = aws_ecs_task_definition.task.arn
  desired_count        = var.desired_count
  force_new_deployment = true
  launch_type          = "FARGATE"

  load_balancer {
    target_group_arn = aws_lb_target_group.api.arn
    container_name   = local.api_container_name
    container_port   = local.api_container_port
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.tasks.arn
    container_name   = local.tasks_container_name
    container_port   = local.tasks_container_port
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.ui.arn
    container_name   = local.ui_container_name
    container_port   = local.ui_container_port
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.landing.arn
    container_name   = local.api_container_name
    container_port   = local.landing_container_port
  }

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.service.id]
    assign_public_ip = false
  }

  lifecycle {
    ignore_changes = [desired_count]
  }
}
