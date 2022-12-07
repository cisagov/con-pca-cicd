module "memory_db" {
  source         = "terraform-aws-modules/memory-db/aws"
  engine_version = "6.2"

  description = "MemoryDB Redis Cluster"
  name        = "redis"

  auto_minor_version_upgrade = true
  node_type                  = "db.t4g.small"
  num_shards                 = 2
  num_replicas_per_shard     = 2

  tls_enabled              = true
  security_group_ids       = [aws_security_group.service.id]
  maintenance_window       = "sun:23:00-mon:01:30"
  snapshot_retention_limit = 7
  snapshot_window          = "05:00-09:00"

  # Users
  users = {
    admin = {
      user_name     = "admin-user"
      access_string = "on ~* &* +@all"
      passwords     = ["YouShouldPickAStrongSecurePassword987!"]
      tags          = { User = "admin" }
    }
    readonly = {
      user_name     = "readonly-user"
      access_string = "on ~* &* -@all +@read"
      passwords     = ["YouShouldPickAStrongSecurePassword123!"]
      tags          = { User = "readonly" }
    }
  }

  # Subnet group
  subnet_group_name        = "redis-subnet-group"
  subnet_group_description = "Redis MemoryDB subnet group"
  subnet_ids               = var.private_subnet_ids

  tags = {
    Terraform   = "true"
    Environment = "${var.app}-${var.env}-redis"
  }
}
