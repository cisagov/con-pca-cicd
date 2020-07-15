
#=================================================
#  VPC and SUBNETS
#=================================================

module "vpc" {
  source     = "github.com/cloudposse/terraform-aws-vpc"
  namespace  = "${var.app}"
  stage      = "${var.env}"
  name       = "vpc"
  cidr_block = "10.0.0.0/16"
}

locals {
  public_cidr_block  = cidrsubnet(module.vpc.vpc_cidr_block, 1, 0)
  private_cidr_block = cidrsubnet(module.vpc.vpc_cidr_block, 1, 1)
}

module "public_subnets" {
  source              = "github.com/cloudposse/terraform-aws-multi-az-subnets"
  namespace           = "${var.app}"
  stage               = "${var.env}"
  name                = "subnet"
  availability_zones  = ["${var.region}a", "${var.region}b"]
  vpc_id              = module.vpc.vpc_id
  cidr_block          = local.public_cidr_block
  type                = "public"
  igw_id              = module.vpc.igw_id
  nat_gateway_enabled = "false"
}

module "private_subnets" {
  source             = "github.com/cloudposse/terraform-aws-multi-az-subnets"
  namespace          = "${var.app}"
  stage              = "${var.env}"
  name               = "subnet"
  availability_zones = ["${var.region}c", "${var.region}d"]
  vpc_id             = module.vpc.vpc_id
  cidr_block         = local.private_cidr_block
  type               = "private"
}


#=================================================
#  S3
#=================================================
module "s3_images" {
  source        = "github.com/cloudposse/terraform-aws-s3-bucket"
  namespace     = "${var.app}"
  stage         = "${var.env}"
  name          = "images"
  acl           = "public-read"
  sse_algorithm = "AES256"
}

#=================================================
#  SELF-SIGNED CERTS
#=================================================
module "certs" {
  source      = "../modules/certs"
  namespace   = var.app
  stage       = var.env
  name        = "alb"
  dns_names   = [module.alb.alb_dns_name]
  common_name = module.alb.alb_dns_name
}

#=================================================
#  APPLICATION LOAD BALANCER
#=================================================
resource "aws_security_group" "alb" {
  name        = "${var.app}-${var.env}-alb-sg"
  description = "Allowed ports into alb"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    "Name" = "${var.app}-${var.env}-alb-sg"
  }
}

module "alb" {
  source             = "github.com/cloudposse/terraform-aws-alb"
  namespace          = "${var.app}"
  stage              = "${var.env}"
  name               = "public"
  http_enabled       = false
  internal           = false
  vpc_id             = module.vpc.vpc_id
  security_group_ids = [aws_security_group.alb.id]
  subnet_ids         = values(module.public_subnets.az_subnet_ids)
}

#=================================================
#  COGNITO USERS
#=================================================
resource "aws_cognito_user_pool" "pool" {
  name = "${var.env}-${var.app}-users"
}
