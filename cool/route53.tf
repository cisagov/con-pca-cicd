resource "aws_route53_zone" "private_zone" {
  name = var.hosted_zone_name

  vpc {
    vpc_id = local.vpc_id
  }
}

resource "aws_route53_zone" "public_zone" {
  name = var.hosted_zone_name
}

resource "aws_route53_record" "public" {
  zone_id = aws_route53_zone.public_zone.zone_id
  name    = var.hosted_zone_name
  type    = "A"

  alias {
    name                   = module.public_alb.alb_dns_name
    zone_id                = module.public_alb.alb_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "internal" {
  zone_id = aws_route53_zone.public_zone.zone_id
  name    = "admin.${var.hosted_zone_name}"
  type    = "CNAME"
  ttl     = "300"
  records = [module.internal_alb.alb_dns_name]
}

resource "aws_route53_record" "internal_private" {
  zone_id = aws_route53_zone.private_zone.zone_id
  name    = "admin.${var.hosted_zone_name}"
  type    = "CNAME"
  ttl     = "300"
  records = [module.internal_alb.alb_dns_name]
}
