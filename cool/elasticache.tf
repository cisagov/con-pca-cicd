module "redis" {
  source  = "cloudposse/elasticache-redis/aws"
  version = "0.48.0"

  stage     = var.env
  namespace = var.app
  name      = "redis"

  availability_zones         = []
  zone_id                    = aws_route53_zone.public_zone.zone_id
  vpc_id                     = local.vpc_id
  allowed_security_group_ids = [aws_security_group.service.id]
  subnets                    = local.private_subnet_ids
  cluster_size               = 2
  instance_type              = "cache.t3.medium"
  apply_immediately          = true
  automatic_failover_enabled = false
  engine_version             = "7.0"
  family                     = "redis7"
  at_rest_encryption_enabled = false
  transit_encryption_enabled = false
}
