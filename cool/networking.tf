# ===========================
# VPC
# ===========================
locals {
  cidr_block         = "10.223.248.0/22" # 10.223.248.0 - 10.223.251.255
  availability_zones = ["${var.region}a", "${var.region}b"]
  az_count           = length(local.availability_zones)
}

# ===========================
# VPC
# ===========================
resource "aws_vpc" "vpc" {
  cidr_block = local.cidr_block

  tags = {
    Name = "${var.app}-${var.env}-vpc"
  }
}

# ===========================
# INTERNET GATEWAY
# ===========================
resource "aws_internet_gateway" "gateway" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "${var.app}-${var.env}-igw"
  }
}

# ===========================
# PUBLIC SUBNET
# ===========================
resource "aws_subnet" "public" {
  count             = local.az_count
  vpc_id            = aws_vpc.vpc.id
  availability_zone = element(local.availability_zones, count.index)
  cidr_block = cidrsubnet(
    local.cidr_block,
    ceil(log(local.az_count * 2, 2)),
    count.index
  )

  tags = {
    Name = "${var.app}-${var.env}-public-${count.index}"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.vpc.id

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
  count          = local.az_count
  subnet_id      = element(aws_subnet.public.*.id, count.index)
  route_table_id = aws_route_table.public.id
}

resource "aws_network_acl" "public" {
  vpc_id     = aws_vpc.vpc.id
  subnet_ids = aws_subnet.public.*.id

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
resource "aws_subnet" "private" {
  count             = local.az_count
  vpc_id            = aws_vpc.vpc.id
  availability_zone = element(local.availability_zones, count.index)
  cidr_block = cidrsubnet(
    local.cidr_block,
    ceil(log(local.az_count * 2, 2)),
    local.az_count + count.index
  )

  tags = {
    Name = "${var.app}-${var.env}-private-${count.index}"
  }
}

resource "aws_route_table" "private" {
  count  = local.az_count
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "${var.app}-${var.env}-private-${element(local.availability_zones, count.index)}"
  }
}

resource "aws_route_table_association" "private" {
  count          = local.az_count
  subnet_id      = element(aws_subnet.private.*.id, count.index)
  route_table_id = element(aws_route_table.private.*.id, count.index)
}

resource "aws_network_acl" "private" {
  vpc_id     = aws_vpc.vpc.id
  subnet_ids = aws_subnet.private.*.id

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
  count = local.az_count
  vpc   = true

  tags = {
    Name = "${var.app}-${var.env}-${element(local.availability_zones, count.index)}"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_nat_gateway" "default" {
  count         = local.az_count
  allocation_id = element(aws_eip.default.*.id, count.index)
  subnet_id     = element(aws_subnet.public.*.id, count.index)

  tags = {
    Name = "${var.app}-${var.env}-${element(local.availability_zones, count.index)}"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route" "default" {
  count                  = local.az_count
  route_table_id         = element(aws_route_table.private.*.id, count.index)
  nat_gateway_id         = element(aws_nat_gateway.default.*.id, count.index)
  destination_cidr_block = "0.0.0.0/0"
}

# ===========================
# TRANSIT GATEWAY
# ===========================
# data "aws_ec2_transit_gateway" "tgw" {
#   filter {
#     name   = "tag:Name"
#     values = [""]
#   }
# }
