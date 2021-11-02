# Document DB
resource "aws_cloudwatch_metric_alarm" "docdb_cpu_high" {
  alarm_name          = "${var.app}-${var.env}-docdb-cpu_high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/DocDB"
  period              = "600"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "Average database CPU utilization over last 10 minutes too high"
  alarm_actions       = ["${aws_sns_topic.notifications.arn}"]
  ok_actions          = ["${aws_sns_topic.notifications.arn}"]

  dimensions = {
    DBClusterIdentifier = aws_docdb_cluster.docdb.cluster_identifier
  }
}

resource "aws_cloudwatch_metric_alarm" "docdb_freeable_memory_too_low" {
  alarm_name          = "${var.app}-${var.env}-docdb-freeable_memory_too_low"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "FreeableMemory"
  namespace           = "AWS/DocDB"
  period              = "600"
  statistic           = "Average"
  threshold           = "64000000" # 64 megabyte in bytes
  alarm_description   = "Average database freeable memory over last 10 minutes too low, performance may suffer"
  alarm_actions       = ["${aws_sns_topic.notifications.arn}"]
  ok_actions          = ["${aws_sns_topic.notifications.arn}"]

  dimensions = {
    DBClusterIdentifier = aws_docdb_cluster.docdb.cluster_identifier
  }
}

resource "aws_cloudwatch_metric_alarm" "docdb_free_local_storage_too_low" {
  alarm_name          = "${var.app}-${var.env}-docdb-free_local_storage_too_low"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "FreeLocalStorage"
  namespace           = "AWS/DocDB"
  period              = "600"
  statistic           = "Average"
  threshold           = "2000000000" # 2 Gigabyte in bytes
  alarm_description   = "Average database free storage space over last 10 minutes too low"
  alarm_actions       = ["${aws_sns_topic.notifications.arn}"]
  ok_actions          = ["${aws_sns_topic.notifications.arn}"]

  dimensions = {
    DBClusterIdentifier = aws_docdb_cluster.docdb.cluster_identifier
  }
}

