# ===========================
# LOCALS
# ===========================
locals {
  api_container_port          = 80
  api_container_protocol      = "HTTP"
  api_load_balancer_port      = 8043
  api_load_balancer_http_port = 8000
  api_name                    = "${var.app}-${var.env}-api"
  api_container_name          = "api"

  api_environment = {
    "SECRET_KEY" : random_string.django_secret_key.result
    "DEBUG" : 0
    "DJANGO_ALLOWED_HOSTS" : "localhost 127.0.0.1 [::1] ${module.internal_alb.alb_dns_name} ${module.public_alb.alb_dns_name} ${aws_route53_record.record.name}"
    "CORS_ORIGIN_WHITELIST" : "https://${aws_route53_record.record.name},https://${aws_route53_record.record.name}:3333"
    "DB_HOST" : module.documentdb.endpoint
    "DB_PORT" : 27017
    "GP_URL" : "https://${aws_route53_record.record.name}:${local.gophish_alb_port}/"
    "WEBHOOK_URL" : "http://${module.internal_alb.alb_dns_name}:8000/api/v1/inboundwebhook/"
    "AWS_S3_IMAGE_BUCKET" : aws_s3_bucket.images.id
    "AWS_S3_EXPORT_BUCKET" : aws_s3_bucket.exports.id
    "DEFAULT_FILE_STORAGE" : "storages.backends.s3boto3.S3Boto3Storage"
    "WORKERS" : var.api_gunicorn_workers
    "COGNITO_DEPLOYMENT_MODE" : "Production"
    "COGNITO_AWS_REGION" : var.region
    "COGNITO_USER_POOL" : aws_cognito_user_pool.pool.id
    "LOCAL_API_KEY" : random_string.local_api_key.result
    "MONGO_TYPE" : "DOCUMENTDB"
    "REPORTS_ENDPOINT" : "https://${aws_route53_record.record.name}"
    "BROWSERLESS_ENDPOINT" : "${aws_lb.network.dns_name}:${local.browserless_port}"
    "EXTRA_BCC_EMAILS" : var.extra_bcc_emails
    "USE_SES" : 1
    "DEFAULT_X_GOPHISH_CONTACT" : "vulnerability@cisa.dhs.gov"
    "DELAY_MINUTES" : var.delay_minutes
    "CYCLE_MINUTES" : var.cycle_minutes
    "MONTHLY_MINUTES" : var.monthly_minutes
    "YEARLY_MINUTES" : var.yearly_minutes
    "DB_USER" : aws_ssm_parameter.docdb_username.value
    "DB_PW" : aws_ssm_parameter.docdb_password.value
    "GP_API_KEY" : data.aws_ssm_parameter.gp_api_key.value
    "GP_SMTP_HOST" : data.aws_ssm_parameter.gp_smtp_host.value
    "GP_SMTP_FROM" : data.aws_ssm_parameter.gp_smtp_from.value
    "GP_SMTP_USER" : data.aws_ssm_parameter.gp_smtp_user.value
    "GP_SMTP_PASS" : data.aws_ssm_parameter.gp_smtp_pass.value
    "GP_LANDING_SUBDOMAIN" : var.gophish_landing_subdomain
    "SMTP_HOST" : data.aws_ssm_parameter.smtp_host.value
    "SMTP_PORT" : data.aws_ssm_parameter.smtp_port.value
    "SMTP_PASS" : data.aws_ssm_parameter.smtp_pass.value
    "SMTP_FROM" : data.aws_ssm_parameter.smtp_from.value
    "SMTP_USER" : data.aws_ssm_parameter.smtp_user.value
    "COGNITO_AUDIENCE" : aws_cognito_user_pool_client.client.id
    "SES_ASSUME_ROLE_ARN" : data.aws_ssm_parameter.ses_assume_role_arn.value
    "DJANGO_SETTINGS_MODULE" : "config.settings"
    "TASKS_QUEUE_URL" : aws_sqs_queue.tasks.id
  }
}



# ===========================
# APP CREDENTIALS
# ===========================
resource "random_string" "django_secret_key" {
  length  = 32
  number  = false
  special = false
  upper   = true
}

resource "random_string" "local_api_key" {
  length  = 32
  number  = false
  special = false
  upper   = true
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
resource "aws_lb_target_group" "api_public" {
  name        = "${local.api_name}-public"
  port        = local.api_container_port
  protocol    = local.api_container_protocol
  target_type = "ip"
  vpc_id      = var.vpc_id

  health_check {
    healthy_threshold   = 3
    interval            = 60
    matcher             = "202,200,307,404"
    path                = "/"
    port                = local.api_container_port
    protocol            = local.api_container_protocol
    unhealthy_threshold = 3
  }
}

resource "aws_lb_target_group" "api_internal" {
  name        = "${local.api_name}-internal"
  port        = local.api_container_port
  protocol    = local.api_container_protocol
  target_type = "ip"
  vpc_id      = var.vpc_id

  health_check {
    healthy_threshold   = 3
    interval            = 60
    matcher             = "202,200,307,404"
    path                = "/"
    port                = local.api_container_port
    protocol            = local.api_container_protocol
    unhealthy_threshold = 3
  }
}


#=========================
# ALB LISTENERS
#=========================
resource "aws_lb_listener" "api" {
  load_balancer_arn = module.public_alb.alb_arn
  port              = local.api_load_balancer_port
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = aws_acm_certificate.cert.arn

  default_action {
    target_group_arn = aws_lb_target_group.api_public.arn
    type             = "forward"
  }
}

resource "aws_lb_listener" "api_http" {
  load_balancer_arn = module.internal_alb.alb_arn
  port              = local.api_load_balancer_http_port
  protocol          = "HTTP"

  default_action {
    target_group_arn = aws_lb_target_group.api_internal.arn
    type             = "forward"
  }
}


# ===========================
# CONTAINER DEFINITION
# ===========================
module "api_container" {
  source          = "github.com/cloudposse/terraform-aws-ecs-container-definition"
  container_name  = local.api_container_name
  container_image = "${var.api_image_repo}:${var.api_image_tag}"
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
    target_group_arn = aws_lb_target_group.api_public.arn
    container_name   = local.api_container_name
    container_port   = local.api_container_port
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.api_internal.arn
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

# ===========================
# SCALING
# ===========================
resource "aws_appautoscaling_target" "api_scaling_target" {
  service_namespace  = "ecs"
  resource_id        = "service/${aws_ecs_cluster.cluster.name}/${aws_ecs_service.api.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  max_capacity       = var.api_max_count
  min_capacity       = var.api_min_count
}

resource "aws_appautoscaling_policy" "api_out" {
  name               = "${local.api_name}-out"
  service_namespace  = aws_appautoscaling_target.api_scaling_target.service_namespace
  resource_id        = aws_appautoscaling_target.api_scaling_target.resource_id
  scalable_dimension = aws_appautoscaling_target.api_scaling_target.scalable_dimension

  step_scaling_policy_configuration {
    adjustment_type         = "ChangeInCapacity"
    cooldown                = 60
    metric_aggregation_type = "Average"
    step_adjustment {
      metric_interval_lower_bound = 0
      scaling_adjustment          = var.api_scale_out_count
    }
  }
}

resource "aws_appautoscaling_policy" "api_in" {
  name               = "${local.api_name}-in"
  service_namespace  = aws_appautoscaling_target.api_scaling_target.service_namespace
  resource_id        = aws_appautoscaling_target.api_scaling_target.resource_id
  scalable_dimension = aws_appautoscaling_target.api_scaling_target.scalable_dimension

  step_scaling_policy_configuration {
    adjustment_type         = "ChangeInCapacity"
    cooldown                = 300
    metric_aggregation_type = "Average"

    step_adjustment {
      metric_interval_upper_bound = 0
      scaling_adjustment          = var.api_scale_in_count
    }
  }
}
