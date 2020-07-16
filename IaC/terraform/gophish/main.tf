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

  allocated_storage  = var.mysql_storage
  database_name      = "gophish"
  database_user      = random_string.mysql_username.result
  database_password  = random_password.mysql_password.result
  database_port      = 3306
  db_parameter_group = "mysql5.7"
  engine             = "mysql"
  engine_version     = "5.7"
  instance_class     = var.mysql_instance_class
  security_group_ids = [aws_security_group.gophish.id]
  subnet_ids         = data.aws_subnet_ids.public.ids
  vpc_id             = data.aws_vpc.vpc.id
}

# ===========================
# FARGATE
# ===========================
module "fargate" {
  source                = "../modules/fargate"
  namespace             = "${var.app}"
  stage                 = "${var.env}"
  name                  = "gophish"
  log_retention         = 7
  iam_server_cert_arn   = data.aws_iam_server_certificate.self.arn
  container_port        = 3333
  vpc_id                = data.aws_vpc.vpc.id
  health_check_interval = 60
  health_check_path     = "/"
  health_check_codes    = "307,202,200,404"
  load_balancer_arn     = data.aws_lb.public.arn
  load_balancer_port    = 3333
  container_image       = "780016325729.dkr.ecr.us-east-1.amazonaws.com/con-pca-gophish:1.0"
  aws_region            = var.region
  cpu                   = 512
  memory                = 1024

  environment = {
    "MYSQL_DATABASE" : "gophish",
    "MYSQL_HOST" : module.rds.instance_endpoint
  }

  secrets = {
    "MYSQL_USER" : aws_ssm_parameter.mysql_username.arn,
    "MYSQL_PASSWORD" : aws_ssm_parameter.mysql_password.arn
  }

  desired_count      = 1
  subnet_ids         = data.aws_subnet_ids.private.ids
  security_group_ids = [aws_security_group.gophish.id]
}

# ===========================
# SECURITY GROUP
# ===========================
resource "aws_security_group" "gophish" {
  name        = "${var.app}-${var.env}-gophish-alb"
  description = "Allow traffic for gophish from alb"
  vpc_id      = data.aws_vpc.vpc.id

  ingress {
    description     = "Allow container port from ALB"
    from_port       = 3333
    to_port         = 3333
    protocol        = "tcp"
    security_groups = [data.aws_security_group.alb.id]
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
