# ===========================
# Certs
# ===========================
module "acm" {
  source      = "github.com/terraform-aws-modules/terraform-aws-acm"
  domain_name = aws_route53_record.record.name
  zone_id     = aws_route53_zone.zone.zone_id
}
