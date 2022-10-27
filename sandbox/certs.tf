# ===========================
# Certs
# ===========================
module "acm" {
  source      = "terraform-aws-modules/acm/aws"
  version     = "3.4.1"
  domain_name = aws_route53_record.domain.name
  zone_id     = data.aws_route53_zone.zone.zone_id
}
