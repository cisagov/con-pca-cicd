# ===========================
# Certs
# ===========================
resource "aws_acm_certificate" "cert" {
  domain_name       = aws_route53_record.record.name
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "validation" {
  allow_overwrite = true
  name            = aws_acm_certificate.cert.domain_validation_options[0].resource_record_name
  records         = [aws_acm_certificate.cert.domain_validation_options[0].resource_record_value]
  ttl             = 60
  type            = aws_acm_certificate.cert.domain_validation_options[0].resource_record_type
  zone_id         = data.aws_route53_zone.zone.zone_id
}

resource "aws_acm_certificate_validation" "validation" {
  certificate_arn         = aws_acm_certificate.cert.arn
  validation_record_fqdns = [aws_route53_record.validation.fqdn]
}
