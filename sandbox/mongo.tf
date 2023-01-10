provider "mongodbatlas" {
  public_key  = ""
  private_key = ""
}

resource "mongodbatlas_cluster" "mongo-cluster" {
  project_id   = "${var.app}-${var.env}"
  name         = "${var.app}-${var.env}-mongo-cluster"
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
