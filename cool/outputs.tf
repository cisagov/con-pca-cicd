output "hosted_zone_name_servers" {
    value = aws_route53_zone.zone.name_servers
}

output "hosted_zone_name" {
    value = aws_route53_zone.zone.name
}

