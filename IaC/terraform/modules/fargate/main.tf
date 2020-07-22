module "label" {
  source     = "github.com/cloudposse/terraform-null-label"
  enabled    = true
  attributes = []
  delimiter  = "-"
  name       = var.name
  namespace  = var.namespace
  stage      = var.stage
  tags       = {}
}

#=========================
# TARGET GROUP
#=========================
resource "aws_lb_target_group" "_" {
  name        = module.label.id
  port        = var.container_port
  protocol    = var.container_protocol
  target_type = "ip"
  vpc_id      = var.vpc_id

  health_check {
    healthy_threshold   = var.health_check_healthy_threshold
    interval            = var.health_check_interval
    matcher             = var.health_check_codes
    path                = var.health_check_path
    port                = var.container_port
    protocol            = var.container_protocol
    unhealthy_threshold = var.health_check_unhealthy_threshold
  }
}

#=========================
# LISTENER
#=========================
resource "aws_lb_listener" "_" {
  load_balancer_arn = var.load_balancer_arn
  port              = var.load_balancer_port
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = var.iam_server_cert_arn

  default_action {
    target_group_arn = aws_lb_target_group._.arn
    type             = "forward"
  }
}

#=========================
# CLUSTER
#=========================
resource "aws_ecs_cluster" "_" {
  name = module.label.id
}


#=========================
# TASK DEFINITION
#=========================
resource "aws_ecs_task_definition" "_" {
  family                   = module.label.id
  container_definitions    = var.container_definition
  cpu                      = var.cpu
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  memory                   = var.memory
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  task_role_arn            = aws_iam_role.ecs_task.arn
}


#=========================
# SERVICE
#=========================
resource "aws_ecs_service" "_" {
  name            = module.label.id
  cluster         = aws_ecs_cluster._.id
  task_definition = aws_ecs_task_definition._.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  load_balancer {
    target_group_arn = aws_lb_target_group._.arn
    container_name   = var.container_name
    container_port   = var.container_port
  }

  network_configuration {
    subnets          = var.subnet_ids
    security_groups  = var.security_group_ids
    assign_public_ip = false
  }
}

#=========================
# IAM ROLES & POLICIES
#=========================
data "aws_iam_policy_document" "ecs_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ecs_execution" {
  name               = "${module.label.id}-ecs-execution"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume_role.json
}

data "aws_iam_policy_document" "ecs_execution" {
  statement {
    actions = [
      "logs:*",
      "ssm:Get*"
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "ecs_execution" {
  name        = "${module.label.id}-ecs-execution"
  description = "Policy for ecs execution"
  policy      = data.aws_iam_policy_document.ecs_execution.json
}

resource "aws_iam_role_policy_attachment" "ecs_execution_base" {
  role       = aws_iam_role.ecs_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy_attachment" "ecs_execution_other" {
  role       = aws_iam_role.ecs_execution.name
  policy_arn = aws_iam_policy.ecs_execution.arn
}

resource "aws_iam_role" "ecs_task" {
  name               = "${module.label.id}-ecs-task"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume_role.json
}

data "aws_iam_policy_document" "ecs_task" {
  statement {
    actions = [
      "s3:*"
    ]

    resources = [
      "*"
    ]
  }
}

resource "aws_iam_policy" "ecs_task" {
  name        = "${module.label.id}-ecs-task"
  description = "Policy for running ecs tasks"
  policy      = data.aws_iam_policy_document.ecs_task.json
}

resource "aws_iam_role_policy_attachment" "ecs_task" {
  role       = aws_iam_role.ecs_task.name
  policy_arn = aws_iam_policy.ecs_task.arn
}
