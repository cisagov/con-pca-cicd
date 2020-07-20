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
  gophish_port = 3333
  landingpage_port = 8080
}

# Cloudwatch Logs Group
resource "aws_cloudwatch_log_group" "_" {
  name              = module.label.id
  retention_in_days = var.log_retention
}

# Load Balancer Target Group
resource "aws_lb_target_group" "gophish" {
  name        = module.label.id
  port        = local.gophish_port
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = var.vpc_id

  health_check {
    healthy_threshold   = var.health_check_healthy_threshold
    interval            = var.health_check_interval
    matcher             = var.health_check_codes
    path                = var.health_check_path
    port                = local.gophish_port
    protocol            = "HTTP"
    unhealthy_threshold = var.health_check_unhealthy_threshold
  }
}

# Load Balancer Listener
resource "aws_lb_listener" "gophish" {
  load_balancer_arn = var.load_balancer_arn
  port              = var.gophish_alb_port
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = var.iam_server_cert_arn

  default_action {
    target_group_arn = aws_lb_target_group.gophish.arn
    type             = "forward"
  }
}

resource "aws_lb_target_group" "landing" {
  name        = "${module.label.id}-landing"
  port        = local.landingpage_port
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = var.vpc_id

  health_check {
    healthy_threshold   = var.health_check_healthy_threshold
    interval            = var.health_check_interval
    matcher             = var.health_check_codes
    path                = var.health_check_path
    port                = local.gophish_port
    protocol            = "HTTP"
    unhealthy_threshold = var.health_check_unhealthy_threshold
  }
}

# Load Balancer Listener
resource "aws_lb_listener" "landing" {
  load_balancer_arn = var.load_balancer_arn
  port              = var.landingpage_alb_port
  protocol          = "HTTP"

  default_action {
    target_group_arn = aws_lb_target_group.landing.arn
    type             = "forward"
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "_" {
  name = module.label.id
}

module "container" {
  source          = "github.com/cloudposse/terraform-aws-ecs-container-definition"
  container_name  = module.label.id
  container_image = var.container_image
  entrypoint      = var.entrypoint
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
      containerPort = local.gophish_port
      hostPort      = local.gophish_port
      protocol      = "tcp"
    },
    {
      containerPort = local.landingpage_port
      hostPort      = local.landingpage_port
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
  cpu                      = var.cpu
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  memory                   = var.memory
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  task_role_arn            = aws_iam_role.ecs_task.arn
}

resource "aws_ecs_service" "_" {
  name            = module.label.id
  cluster         = aws_ecs_cluster._.id
  task_definition = aws_ecs_task_definition._.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  load_balancer {
    target_group_arn = aws_lb_target_group.landing.arn
    container_name   = module.label.id
    container_port   = local.landingpage_port
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.gophish.arn
    container_name   = module.label.id
    container_port   = local.gophish_port
  }

  network_configuration {
    subnets          = var.subnet_ids
    security_groups  = var.security_group_ids
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
