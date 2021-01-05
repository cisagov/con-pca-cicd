# ===========================
# Certs
# ===========================
module "web_certs" {
  source      = "github.com/terraform-aws-modules/terraform-aws-acm"
  domain_name = aws_route53_record.sharedservices_internal_web.name
  zone_id     = aws_route53_zone.public_zone.zone_id
}

module "gophish_certs" {
  source      = "github.com/terraform-aws-modules/terraform-aws-acm"
  domain_name = aws_route53_record.sharedservices_internal_gophish.name
  zone_id     = aws_route53_zone.public_zone.zone_id
}

module "api_certs" {
  source      = "github.com/terraform-aws-modules/terraform-aws-acm"
  domain_name = aws_route53_record.sharedservices_internal_api.name
  zone_id     = aws_route53_zone.public_zone.zone_id
}

module "public_certs" {
  source      = "github.com/terraform-aws-modules/terraform-aws-acm"
  domain_name = aws_route53_record.public.name
  zone_id     = aws_route53_zone.public_zone.zone_id
}
