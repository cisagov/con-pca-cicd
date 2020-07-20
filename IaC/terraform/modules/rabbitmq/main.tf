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

locals {
  rabbitmq_port = 5672
}

resource "aws_lb_target_group" "_" {
  name        = module.label.id
  port        = local.rabbitmq_port
  protocol    = "TCP"
  target_type = "ip"
  vpc_id      = var.vpc_id

  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 2
    interval            = 30
    port                = local.rabbitmq_port
    protocol            = "TCP"
  }
}

resource "aws_lb" "network" {
  name                             = module.label.id
  enable_cross_zone_load_balancing = true
  idle_timeout                     = 60
  internal                         = true
  load_balancer_type               = "network"
  subnets                          = var.private_subnet_ids
}

resource "aws_lb_listener" "_" {
  load_balancer_arn = aws_lb.network.arn
  port              = local.rabbitmq_port
  protocol          = "TCP"

  default_action {
    target_group_arn = aws_lb_target_group._.arn
    type             = "forward"
  }
}

resource "aws_security_group" "rabbitmq" {
  name        = module.label.id
  description = "Allow traffic for rabbitmq from nlb"
  vpc_id      = var.vpc_id

  ingress {
    description = "Allow container port from ALB"
    from_port   = local.rabbitmq_port
    to_port     = local.rabbitmq_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    self        = true
  }

  egress {
    description = "Allow outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    "Name" = module.label.id
  }
}

resource "aws_ecs_cluster" "_" {
  name = module.label.id
}

resource "aws_cloudwatch_log_group" "_" {
  name              = module.label.id
  retention_in_days = var.log_retention
}

module "container" {
  source          = "github.com/cloudposse/terraform-aws-ecs-container-definition"
  container_name  = module.label.id
  container_image = "docker.io/rabbitmq:3.8"
  essential       = "true"
  log_configuration = {
    logDriver = "awslogs"
    options = {
      awslogs-region        = var.aws_region
      awslogs-group         = aws_cloudwatch_log_group._.name
      awslogs-stream-prefix = "/ecs/${var.name}"
    }
  }
  port_mappings = [
    {
      containerPort = local.rabbitmq_port
      hostPort      = local.rabbitmq_port
      protocol      = "tcp"
    }
  ]

  environment = [
    for key in keys(var.environment) :
    {
      name  = key
      value = var.environment[key]
    }
  ]

  secrets = [
    for key in keys(var.secrets) :
    {
      name      = key
      valueFrom = var.secrets[key]
    }
  ]
}

resource "aws_ecs_task_definition" "_" {
  family                   = module.label.id
  container_definitions    = module.container.json
  cpu                      = 512
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  memory                   = 1024
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  task_role_arn            = aws_iam_role.ecs_task.arn
}

resource "aws_ecs_service" "_" {
  name            = module.label.id
  cluster         = aws_ecs_cluster._.id
  task_definition = aws_ecs_task_definition._.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  load_balancer {
    target_group_arn = aws_lb_target_group._.arn
    container_name   = module.label.id
    container_port   = local.rabbitmq_port
  }

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.rabbitmq.id]
    assign_public_ip = false
  }
}


# IAM
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
