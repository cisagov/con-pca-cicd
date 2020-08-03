
#=================================================
#  VPC and SUBNETS
#=================================================

module "vpc" {
  source     = "github.com/cloudposse/terraform-aws-vpc"
  namespace  = "${var.app}"
  name       = "vpc"
  cidr_block = "10.0.0.0/16"
}

locals {
  public_cidr_block  = cidrsubnet(module.vpc.vpc_cidr_block, 1, 0)
  private_cidr_block = cidrsubnet(module.vpc.vpc_cidr_block, 1, 1)
}

module "subnets" {
  source              = "github.com/cloudposse/terraform-aws-dynamic-subnets"
  namespace           = var.app
  name                = "subnet"
  vpc_id              = module.vpc.vpc_id
  igw_id              = module.vpc.igw_id
  cidr_block          = "10.0.0.0/16"
  availability_zones  = ["${var.region}a", "${var.region}b"]
  nat_gateway_enabled = true
}
