output "json" {
  value = "[${module.container.json_map}]"
}

output "json_map" {
  value = module.container.json_map
}
