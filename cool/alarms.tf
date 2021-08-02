# #=========================
# # API FARGATE
# #=========================
resource "aws_cloudwatch_metric_alarm" "api_cpu_high" {
  alarm_name          = "${var.app}-${var.env}-api-cpu-high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "CPUUtilization"
  namespace           = "AWS/ECS"
  period              = 300
  statistic           = "Average"
  threshold           = 80
  alarm_description   = "Average API CPU Utilization over 80%"
  alarm_actions       = [aws_sns_topic.notifications.arn, aws_appautoscaling_policy.api_out.arn]
}

resource "aws_cloudwatch_metric_alarm" "api_cpu_low" {
  alarm_name          = "${var.app}-${var.env}-api-cpu-low"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = 1
  metric_name         = "CPUUtilization"
  namespace           = "AWS/ECS"
  period              = 300
  statistic           = "Average"
  threshold           = 30
  alarm_description   = "Average API CPU utilization under 30%"
  alarm_actions       = [aws_sns_topic.notifications.arn, aws_appautoscaling_policy.api_in.arn]
}

#=========================
# GOPHISH RDS
#=========================
resource "aws_cloudwatch_metric_alarm" "gophish_rds_cpu_high" {
  alarm_name          = "${var.app}-${var.env}-gophish-rds-cpu_high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/RDS"
  period              = "600"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "Average database CPU utilization over last 10 minutes too high"
  alarm_actions       = ["${aws_sns_topic.notifications.arn}"]
  ok_actions          = ["${aws_sns_topic.notifications.arn}"]

  dimensions = {
    DBInstanceIdentifier = module.rds.instance_id
  }
}

resource "aws_cloudwatch_metric_alarm" "gophish_rds_freeable_memory_low" {
  alarm_name          = "${var.app}-${var.env}-gophish-rds-freeable_memory_too_low"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "FreeableMemory"
  namespace           = "AWS/RDS"
  period              = "600"
  statistic           = "Average"
  threshold           = "64000000" # 64 megabyte in bytes
  alarm_description   = "Average database freeable memory over last 10 minutes too low, performance may suffer"
  alarm_actions       = ["${aws_sns_topic.notifications.arn}"]
  ok_actions          = ["${aws_sns_topic.notifications.arn}"]

  dimensions = {
    DBInstanceIdentifier = module.rds.instance_id
  }
}

resource "aws_cloudwatch_metric_alarm" "gophish_rds_free_storage_space_too_low" {
  alarm_name          = "${var.app}-${var.env}-gophish-rds-free_storage_space_threshold"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "FreeStorageSpace"
  namespace           = "AWS/RDS"
  period              = "600"
  statistic           = "Average"
  threshold           = "2000000000" # 2 Gigabyte in bytes
  alarm_description   = "Average database free storage space over last 10 minutes too low"
  alarm_actions       = ["${aws_sns_topic.notifications.arn}"]
  ok_actions          = ["${aws_sns_topic.notifications.arn}"]

  dimensions = {
    DBInstanceIdentifier = module.rds.instance_id
  }
}

#=========================
# DOCUMENT DB
#=========================
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
    DBClusterIdentifier = module.documentdb.cluster_name
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
    DBClusterIdentifier = module.documentdb.cluster_name
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
    DBClusterIdentifier = module.documentdb.cluster_name
  }
}

