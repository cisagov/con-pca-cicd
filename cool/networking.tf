# ===========================
# VPC
# ===========================
locals {
  vpc_id             = data.terraform_remote_state.cool_pca_networking.outputs.vpc.id
  private_subnet_ids = values(data.terraform_remote_state.cool_pca_networking.outputs.private_subnets).*.id
  public_subnet_ids  = values(data.terraform_remote_state.cool_pca_networking.outputs.public_subnets).*.id
  transit_gateway_id = data.terraform_remote_state.cool_pca_networking.outputs.transit_gateway_id
  cool_cidr_block    = "10.128.0.0/16"
}

# ===========================
# INTERNET GATEWAY
# ===========================
resource "aws_internet_gateway" "gateway" {
  vpc_id = local.vpc_id

  tags = {
    Name = "${var.app}-${var.env}-igw"
  }
}

# ===========================
# PUBLIC ROUTE
# ===========================
resource "aws_route_table" "public" {
  vpc_id = local.vpc_id

  tags = {
    Name = "${var.app}-${var.env}-public"
  }
}

resource "aws_route" "public" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.gateway.id
}

resource "aws_route_table_association" "public" {
  count          = length(local.public_subnet_ids)
  subnet_id      = element(local.public_subnet_ids, count.index)
  route_table_id = aws_route_table.public.id
}

resource "aws_network_acl" "public" {
  vpc_id     = local.vpc_id
  subnet_ids = local.public_subnet_ids

  egress {
    rule_no    = 100
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 0
    to_port    = 0
    protocol   = "-1"
  }

  ingress {
    rule_no    = 100
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 0
    to_port    = 0
    protocol   = "-1"
  }
}

# ===========================
# PRIVATE SUBNET
# ===========================

resource "aws_route_table" "private" {
  count  = length(local.public_subnet_ids)
  vpc_id = local.vpc_id

  tags = {
    Name = "${var.app}-${var.env}-private-${count.index}"
  }
}

resource "aws_route_table_association" "private" {
  count          = length(local.public_subnet_ids)
  subnet_id      = element(local.private_subnet_ids, count.index)
  route_table_id = element(aws_route_table.private.*.id, count.index)
}

resource "aws_route" "cool" {
  count                  = length(local.private_subnet_ids)
  route_table_id         = element(aws_route_table.private.*.id, count.index)
  destination_cidr_block = local.cool_cidr_block
  transit_gateway_id     = local.transit_gateway_id
}

resource "aws_network_acl" "private" {
  vpc_id     = local.vpc_id
  subnet_ids = local.private_subnet_ids

  egress {
    rule_no    = 100
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 0
    to_port    = 0
    protocol   = "-1"
  }

  ingress {
    rule_no    = 100
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 0
    to_port    = 0
    protocol   = "-1"
  }
}

# ===========================
# NAT GATEWAY
# ===========================
resource "aws_eip" "default" {
  count = length(local.public_subnet_ids)
  vpc   = true

  tags = {
    Name = "${var.app}-${var.env}-${count.index}"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_nat_gateway" "default" {
  count         = length(local.public_subnet_ids)
  allocation_id = element(aws_eip.default.*.id, count.index)
  subnet_id     = element(local.public_subnet_ids, count.index)

  tags = {
    Name = "${var.app}-${var.env}-${count.index}"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route" "default" {
  count                  = length(local.public_subnet_ids)
  route_table_id         = element(aws_route_table.private.*.id, count.index)
  nat_gateway_id         = element(aws_nat_gateway.default.*.id, count.index)
  destination_cidr_block = "0.0.0.0/0"
}
