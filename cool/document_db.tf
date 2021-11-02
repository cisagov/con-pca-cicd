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

# Document DB Subnet Group
resource "aws_docdb_subnet_group" "docdb" {
  name       = "${var.app}-${var.env}-docdb"
  subnet_ids = local.private_subnet_ids
}

# Document DB Parameter Group
resource "aws_docdb_cluster_parameter_group" "docdb" {
  family = "docdb3.6"
  name   = "${var.env}-${var.app}-docdb"
}

# Document DB Cluster
resource "aws_docdb_cluster" "docdb" {
  cluster_identifier              = "${var.app}-${var.env}-docdb"
  db_cluster_parameter_group_name = aws_docdb_cluster_parameter_group.docdb.name
  db_subnet_group_name            = aws_docdb_subnet_group.docdb.name
  engine                          = "docdb"
  master_username                 = random_string.docdb_username.result
  master_password                 = random_password.docdb_password.result
  skip_final_snapshot             = true
}

# Document DB Instance
resource "aws_docdb_cluster_instance" "docdb" {
  count              = 1
  identifier         = "${var.app}-${var.env}-docdb-${count.index}"
  cluster_identifier = aws_docdb_cluster.docdb.id
  instance_class     = var.documentdb_instance_class
}




