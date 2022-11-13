# Username and password for connecting to document db
resource "random_string" "docdb_username" {
  length  = 8
  number  = false
  special = false
  upper   = false
}

resource "random_password" "docdb_password" {
  length           = 32
  special          = true
  override_special = "!_#&"
}

# Document DB Module
module "documentdb" {
  source  = "cloudposse/documentdb-cluster/aws"
  version = "0.14.1"

  namespace = var.app
  stage     = var.env
  name      = "db"

  allowed_security_groups = [aws_security_group.service.id]
  cluster_family          = "docdb3.6"
  cluster_size            = 1
  instance_class          = var.documentdb_instance_class
  master_username         = random_string.docdb_username.result
  master_password         = random_password.docdb_password.result
  skip_final_snapshot     = true
  snapshot_identifier     = var.documentdb_snapshot_identifier
  subnet_ids              = local.private_subnet_ids
  vpc_id                  = local.vpc_id
}

module "docdb" {
  source                  = "git::https://github.com/cloudposse/terraform-aws-documentdb-cluster.git?ref=tags/0.13.0"
  stage                   = var.env
  namespace               = var.app
  name                    = "docdb"
  cluster_family          = "docdb4.0"
  cluster_size            = var.documentdb_cluster_size
  master_username         = random_string.docdb_username.result
  master_password         = random_password.docdb_password.result
  instance_class          = var.documentdb_instance_class
  vpc_id                  = var.vpc_id
  subnet_ids              = var.private_subnet_ids
  allowed_cidr_blocks     = ["10.0.0.0/8"]
  allowed_security_groups = [aws_security_group.service.id]
  skip_final_snapshot     = true
}
