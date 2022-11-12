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
  source  = "cloudposse/documentdb-cluster/aws"
  version = "0.13.0"

  namespace = var.app
  stage     = var.env
  name      = "docdb"

  allowed_security_groups = [aws_security_group.service.id]
  cluster_family          = "docdb4.0"
  cluster_size            = 1
  instance_class          = var.documentdb_instance_class
  master_username         = random_string.docdb_username.result
  master_password         = random_password.docdb_password.result
  skip_final_snapshot     = true
  snapshot_identifier     = var.documentdb_snapshot_identifier
  subnet_ids              = local.private_subnet_ids
  vpc_id                  = local.vpc_id
}
