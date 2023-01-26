resource "random_string" "mongodb_username" {
  length  = 8
  numeric = false
  special = false
  upper   = false
}

resource "aws_ssm_parameter" "mongodb_username" {
  name        = "/${var.env}/${var.app}/mongodb/username/master"
  description = "The username for mongo atlas"
  type        = "SecureString"
  value       = random_string.mongodb_username.result
}

resource "random_password" "mongodb_password" {
  length           = 32
  special          = true
  override_special = "!_#&"
}

resource "aws_ssm_parameter" "mongodb_password" {
  name        = "/${var.env}/${var.app}/mongodb/password/master"
  description = "The password for mongo atlas"
  type        = "SecureString"
  value       = random_password.mongodb_password.result
}


provider "mongodbatlas" {
  public_key  = var.atlas_public_key
  private_key = var.atlas_private_key
}

resource "mongodbatlas_project" "con-pca" {
  name   = "con-pca-${var.env}"
  org_id = var.atlasorgid
}

resource "mongodbatlas_cluster" "mongo-cluster" {
  project_id   = mongodbatlas_project.con-pca.id
  name         = "${var.app}-${var.env}-cluster"
  cluster_type = "REPLICASET"
  replication_specs {
    num_shards = 1
    regions_config {
      region_name     = "US_EAST_1"
      electable_nodes = 3
      priority        = 7
      read_only_nodes = 0
    }
  }
  cloud_backup                 = true
  auto_scaling_disk_gb_enabled = true
  mongo_db_major_version       = "6.0"

  # Provider Settings "block"
  provider_name               = "AWS"
  disk_size_gb                = 10
  provider_instance_size_name = "M10"
}

resource "mongodbatlas_database_user" "db-user" {
  username           = random_string.mongodb_username.result
  password           = random_password.mongodb_password.result
  auth_database_name = "admin"
  project_id         = mongodbatlas_project.con-pca.id
  roles {
    role_name     = "readWrite"
    database_name = "pca"
  }
  depends_on = [mongodbatlas_project.con-pca]
}
