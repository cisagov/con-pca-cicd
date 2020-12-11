resource "aws_route53_zone" "zone" {
  name = var.hosted_zone_name

  depends_on = [aws_iam_role_policy_attachment.policy]
}

resource "aws_route53_record" "record" {
  zone_id = aws_route53_zone.zone.zone_id
  name    = var.hosted_zone_name
  type    = "A"

  alias {
    name                   = module.public_alb.alb_dns_name
    zone_id                = module.public_alb.alb_zone_id
    evaluate_target_health = false
  }
}
