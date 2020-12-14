# ===================================
# SQS
# ===================================
resource "aws_sqs_queue" "tasks" {
  name                       = "${var.app}-${var.env}-tasks"
  visibility_timeout_seconds = var.tasks_timeout
}
