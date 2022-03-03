resource "aws_cloudwatch_event_rule" "stpped_tasks" {
  name        = "${var.app}-${var.env}-stopped_tasks"
  description = "Send notifications to SNS when an ECS task stops for ${var.app}-${var.env}"

  event_pattern = <<EOF
{
    "source": ["aws.ecs"],
    "detail-type": ["ECS Task State Change"],
    "detail": {
        "clusterArn": ["${aws_ecs_cluster.cluster.arn}"],
        "lastStatus": ["STOPPED"]
    }
}
EOF
}

resource "aws_cloudwatch_event_target" "stopped_tasks_target" {
  rule = aws_cloudwatch_event_rule.stpped_tasks.name
  arn  = aws_sns_topic.notifications.arn

  input_transformer {
    input_paths = {
      status        = "$.detail.lastStatus"
      stopCode      = "$.detail.stopCode"
      stoppedReason = "$.detail.stoppedReason"
    }

    input_template = "\"${var.app}-${var.env} task stopped - <stoppedReason>\""
  }
}
