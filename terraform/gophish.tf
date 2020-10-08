# ===========================
# LOCALS
# ===========================
locals {
  gophish_port     = 3333
  landingpage_port = 8080

  gophish_alb_port     = 3333
  landingpage_alb_port = 443

  gophish_environment = {
    "MYSQL_DATABASE" : "gophish",
    "MYSQL_HOST" : module.rds.instance_endpoint
  }

  gophish_secrets = {
    "MYSQL_USER" : aws_ssm_parameter.mysql_username.arn,
    "MYSQL_PASSWORD" : aws_ssm_parameter.mysql_password.arn
  }

  gophish_container_name = "gophish"
}

# ===========================
# CREDENTIALS
# ===========================
resource "random_string" "mysql_username" {
  length  = 8
  number  = false
  special = false
  upper   = false
}

resource "aws_ssm_parameter" "mysql_username" {
  name        = "/${var.env}/${var.app}/gophish/database/username/master"
  description = "The username for gophish mysql database"
  type        = "SecureString"
  value       = random_string.mysql_username.result
}

resource "random_password" "mysql_password" {
  length           = 32
  special          = true
  override_special = "!_#&"
}

resource "aws_ssm_parameter" "mysql_password" {
  name        = "/${var.env}/${var.app}/gophish/database/password/master"
  description = "The password for gophish mysql database"
  type        = "SecureString"
  value       = random_password.mysql_password.result
}

# ===========================
# RDS (MySQL Database)
# ===========================
module "rds" {
  source    = "github.com/cloudposse/terraform-aws-rds"
  namespace = "${var.app}"
  stage     = "${var.env}"
  name      = "gophish"

  allocated_storage  = var.gophish_mysql_storage
  database_name      = "gophish"
  database_user      = random_string.mysql_username.result
  database_password  = random_password.mysql_password.result
  database_port      = 3306
  db_parameter_group = "mysql5.7"
  engine             = "mysql"
  engine_version     = "5.7"
  instance_class     = var.gophish_mysql_instance_class
  security_group_ids = [aws_security_group.gophish.id]
  subnet_ids         = var.public_subnet_ids
  vpc_id             = var.vpc_id
}

# ===========================
# CLOUDWATCH LOGS
# ===========================
resource "aws_cloudwatch_log_group" "gophish" {
  name              = "${var.app}-${var.env}-gophish"
  retention_in_days = var.log_retention_days
}

# ===========================
# ALB TARGET GROUPS
# ===========================
resource "aws_lb_target_group" "gophish" {
  name        = "${var.app}-${var.env}-gophish"
  port        = local.gophish_port
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = var.vpc_id

  health_check {
    healthy_threshold   = 3
    interval            = 60
    matcher             = "200,307"
    path                = "/"
    port                = local.gophish_port
    protocol            = "HTTP"
    unhealthy_threshold = 3
  }
}

resource "aws_lb_target_group" "landing" {
  name        = "${var.app}-${var.env}-landing"
  port        = local.landingpage_port
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = var.vpc_id

  health_check {
    healthy_threshold   = 3
    interval            = 60
    matcher             = "200,307"
    path                = "/"
    port                = local.gophish_port
    protocol            = "HTTP"
    unhealthy_threshold = 3
  }
}

# ===========================
# ALB LISTENERS
# ===========================
resource "aws_lb_listener" "gophish" {
  load_balancer_arn = module.public_alb.alb_arn
  port              = local.gophish_alb_port
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = aws_acm_certificate.cert.arn

  default_action {
    target_group_arn = aws_lb_target_group.gophish.arn
    type             = "forward"
  }
}

resource "aws_lb_listener" "landing" {
  load_balancer_arn = module.public_alb.alb_arn
  port              = local.landingpage_alb_port
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = aws_acm_certificate.cert.arn

  default_action {
    target_group_arn = aws_lb_target_group.landing.arn
    type             = "forward"
  }
}

# ===========================
# CONTAINER DEFINITION
# ===========================
module "gophish_container" {
  source          = "github.com/cloudposse/terraform-aws-ecs-container-definition"
  container_name  = local.gophish_container_name
  container_image = "${var.gophish_image_repo}:${var.gophish_image_tag}"
  essential       = "true"
  log_configuration = {
    logDriver = "awslogs"
    options = {
      awslogs-region        = var.region
      awslogs-group         = aws_cloudwatch_log_group.gophish.name
      awslogs-stream-prefix = "/ecs/gophish"
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
    for key in keys(local.gophish_environment) :
    {
      name  = key
      value = local.gophish_environment[key]
    }
  ]

  secrets = [
    for key in keys(local.gophish_secrets) :
    {
      name      = key
      valueFrom = local.gophish_secrets[key]
    }
  ]
}

# ===========================
# FARGAGE TASK DEFINITION
# ===========================
resource "aws_ecs_task_definition" "gophish" {
  family                   = "${var.env}-${var.app}-gophish"
  container_definitions    = module.gophish_container.json_map_encoded_list
  cpu                      = var.gophish_cpu
  execution_role_arn       = module.gophish_roles.execution_role_arn
  memory                   = var.gophish_memory
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  task_role_arn            = module.gophish_roles.task_role_arn
}

# ===========================
# FARGAGE SERVICE
# ===========================
resource "aws_ecs_service" "gophish" {
  name            = "gophish"
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.gophish.arn
  desired_count   = var.gophish_count
  launch_type     = "FARGATE"

  load_balancer {
    target_group_arn = aws_lb_target_group.landing.arn
    container_name   = local.gophish_container_name
    container_port   = local.landingpage_port
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.gophish.arn
    container_name   = local.gophish_container_name
    container_port   = local.gophish_port
  }

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.gophish.id]
    assign_public_ip = false
  }
}

# ===========================
# IAM ROLES
# ===========================
module "gophish_roles" {
  source      = "./fargate_roles"
  namespace   = var.app
  stage       = var.env
  name        = "gophish"
  permissions = ["s3:*"]
}

# ===========================
# SECURITY GROUP
# ===========================
resource "aws_security_group" "gophish" {
  name        = "${var.app}-${var.env}-gophish-alb"
  description = "Allow traffic for gophish from alb"
  vpc_id      = var.vpc_id

  ingress {
    description     = "Allow container port from ALB"
    from_port       = 3333
    to_port         = 3333
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
    self            = true
  }

  ingress {
    description     = "Allow container port from ALB"
    from_port       = 8080
    to_port         = 8080
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
    "Name" = "${var.app}-${var.env}-gophish-alb"
  }

}
