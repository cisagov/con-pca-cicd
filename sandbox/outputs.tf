output "redis_cluster_endpoint" {
  value       = module.memory_db.cluster_endpoint_address
  description = "MemoryDB Redis primary endpoint"
}

output "redis_cluster_endpoint_port" {
  description = "Port number that the cluster configuration endpoint is listening on"
  value       = module.memory_db.cluster_endpoint_port
}
