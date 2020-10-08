# ===========================
# ROUTE 53
# ===========================
resource "aws_route53_record" "record" {
  zone_id = data.aws_route53_zone.zone.zone_id
  name    = "${var.app}.${var.env}.${data.aws_route53_zone.zone.name}"
  type    = "CNAME"
  ttl     = "300"
  records = [module.public_alb.alb_dns_name]
}
