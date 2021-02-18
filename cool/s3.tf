# ===========================
# S3
# ===========================
resource "aws_s3_bucket" "images" {
  bucket = "${var.app}-${var.env}-template-images"
  acl    = "public-read"
  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Public",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::${var.app}-${var.env}-template-images/*"
    }
  ]
}
POLICY
}

resource "aws_s3_bucket" "exports" {
  bucket = "${var.app}-${var.env}-exports"
  acl    = "private"
}
