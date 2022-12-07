output "redis_cluster_endpoint" {
  value       = module.redis.endpoint
  description = "Redis primary endpoint"
}

output "redis_cluster_host" {
  value       = module.redis.host
  description = "Redis hostname"
}
