resource "aws_sns_topic" "notifications" {
  name = "${var.app}-${var.env}-notifications"
}