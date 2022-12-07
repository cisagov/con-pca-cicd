output "redis_cluster_endpoint" {
  value       = module.memory_db.endpoint
  description = "MemoryDB Redis primary endpoint"
}

output "redis_cluster_host" {
  value       = module.memory_db.host
  description = "MemoryDB Redis hostname"
}
