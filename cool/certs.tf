# Certs for internal load balancer
module "internal_certs" {
  source      = "terraform-aws-modules/acm/aws"
  version     = "3.4.1"
  domain_name = aws_route53_record.sharedservices_internal_web.name
  zone_id     = aws_route53_zone.public_zone.zone_id
}

# # Certs for public load balancer
# module "public_certs" {
#   source      = "terraform-aws-modules/acm/aws"
#   version     = "3.4.1"
#   domain_name = aws_route53_record.public.name
#   zone_id     = aws_route53_zone.public_zone.zone_id
# }
