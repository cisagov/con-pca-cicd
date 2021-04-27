# ===========================
# Certs
# ===========================
module "web_certs" {
  source      = "terraform-aws-modules/acm/aws"
  version     = "~> v2.14.0"
  domain_name = aws_route53_record.sharedservices_internal_web.name
  zone_id     = aws_route53_zone.public_zone.zone_id
}

module "gophish_certs" {
  source      = "terraform-aws-modules/acm/aws"
  version     = "~> v2.14.0"
  domain_name = aws_route53_record.sharedservices_internal_gophish.name
  zone_id     = aws_route53_zone.public_zone.zone_id
}

module "api_certs" {
  source      = "terraform-aws-modules/acm/aws"
  version     = "~> v2.14.0"
  domain_name = aws_route53_record.sharedservices_internal_api.name
  zone_id     = aws_route53_zone.public_zone.zone_id
}

module "public_certs" {
  source      = "terraform-aws-modules/acm/aws"
  version     = "~> v2.14.0"
  domain_name = aws_route53_record.public.name
  zone_id     = aws_route53_zone.public_zone.zone_id
}
