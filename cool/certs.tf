# ===========================
# Certs
# ===========================
module "internal_certs" {
  source      = "github.com/terraform-aws-modules/terraform-aws-acm"
  domain_name = aws_route53_record.sharedservices_internal.name
  zone_id     = aws_route53_zone.public_zone.zone_id
}

module "public_certs" {
  source      = "github.com/terraform-aws-modules/terraform-aws-acm"
  domain_name = aws_route53_record.public.name
  zone_id     = aws_route53_zone.public_zone.zone_id
}
