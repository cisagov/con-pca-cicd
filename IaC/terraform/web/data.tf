data "aws_vpc" "vpc" {
  tags = {
    Name = "${var.app}-${var.env}-vpc"
  }
}

data "aws_subnet_ids" "public" {
  vpc_id = data.aws_vpc.vpc.id

  tags = {
    Name = "${var.app}-${var.env}-subnet-public*"
  }
}

data "aws_lb" "public" {
  name = "${var.app}-${var.env}-public"
}

data "aws_security_group" "alb" {
  name = "${var.app}-${var.env}-alb-sg"
}

data "aws_cognito_user_pools" "users" {
  name = "${var.env}-${var.app}-users"
}

data "aws_iam_server_certificate" "self" {
  name = "${var.app}-${var.env}-alb"
}
