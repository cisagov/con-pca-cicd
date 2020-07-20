module "label" {
  source     = "github.com/cloudposse/terraform-null-label"
  enabled    = true
  attributes = []
  delimiter  = "-"
  name       = var.name
  namespace  = var.namespace
  stage      = var.stage
  tags       = {}
}

resource "tls_private_key" "_" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

resource "tls_self_signed_cert" "_" {
  key_algorithm         = tls_private_key._.algorithm
  private_key_pem       = tls_private_key._.private_key_pem
  validity_period_hours = 720
  allowed_uses = [
    "key_encipherment",
    "digital_signature",
    "server_auth"
  ]

  dns_names = var.dns_names

  subject {
    common_name  = var.common_name
    organization = module.label.id
  }
}

resource "aws_iam_server_certificate" "_" {
  name             = module.label.id
  certificate_body = tls_self_signed_cert._.cert_pem
  private_key      = tls_private_key._.private_key_pem
}
