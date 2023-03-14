# Document DB
resource "aws_cloudwatch_metric_alarm" "ecs_cpu_high" {
  alarm_name          = "${var.app}-${var.env}-cpu_high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/ECS"
  period              = "600"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "Average CPU utilization over last 10 minutes too high"
  alarm_actions       = ["${aws_sns_topic.notifications.arn}"]
  ok_actions          = ["${aws_sns_topic.notifications.arn}"]

  dimensions = {
    ClusterName = "${var.app}-${var.env}"
  }
}

resource "aws_cloudwatch_metric_alarm" "ecs_memory_high" {
  alarm_name          = "${var.app}-${var.env}-memory-high"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "MemoryUtilization"
  namespace           = "AWS/ECS"
  period              = "600"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "Average Memory utilization over last 10 minutes too high"
  alarm_actions       = ["${aws_sns_topic.notifications.arn}"]
  ok_actions          = ["${aws_sns_topic.notifications.arn}"]

  dimensions = {
    ClusterName = "${var.app}-${var.env}"
  }
}
