locals {
  cool_dns_private_zone = data.terraform_remote_state.sharedservices_networking.outputs.private_zone
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

resource "aws_route53_record" "sharedservices_public" {
  provider = aws.dns_sharedservices

  zone_id = local.cool_dns_private_zone.zone_id
  name    = var.hosted_zone_name
  type    = "A"

  alias {
    name                   = module.public_alb.alb_dns_name
    zone_id                = module.public_alb.alb_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "sharedservices_internal" {
  provider = aws.dns_sharedservices

  zone_id = local.cool_dns_private_zone.zone_id
  name    = "admin.${var.hosted_zone_name}"
  type    = "A"

  alias {
    name                   = aws_lb.internal.dns_name
    zone_id                = aws_lb.internal.zone_id
    evaluate_target_health = false
  }
}
