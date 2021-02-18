# ===================================
# Lambda Layer
# ===================================
data "archive_file" "layer" {
  type        = "zip"
  source_dir  = "${path.module}/layer/"
  output_path = "${path.module}/output/layer.zip"
}

resource "aws_lambda_layer_version" "layer" {
  filename         = data.archive_file.layer.output_path
  source_code_hash = data.archive_file.layer.output_path
  layer_name       = "${var.app}-${var.env}-layer"

  compatible_runtimes = ["python3.8"]

  lifecycle {
    create_before_destroy = true
  }
}

# ===================================
# Lambda Function
# ===================================
data "archive_file" "code" {
  type        = "zip"
  source_dir  = "${path.module}/../../con-pca-api/src/"
  output_path = "${path.module}/output/code.zip"
}

resource "aws_lambda_function" "process_tasks" {
  filename         = data.archive_file.code.output_path
  function_name    = "${var.app}-${var.env}-process-tasks"
  handler          = "lambda_functions.tasks.process_tasks.lambda_handler"
  role             = aws_iam_role.lambda_exec_role.arn
  memory_size      = var.tasks_memory
  runtime          = "python3.8"
  source_code_hash = data.archive_file.code.output_base64sha256
  timeout          = var.tasks_timeout

  layers = [aws_lambda_layer_version.layer.arn]

  environment {
    variables = local.api_environment
  }

  vpc_config {
    subnet_ids         = local.private_subnet_ids
    security_group_ids = [aws_security_group.api.id]
  }
}

resource "aws_lambda_function" "queue_tasks" {
  filename         = data.archive_file.code.output_path
  function_name    = "${var.app}-${var.env}-queue-tasks"
  handler          = "lambda_functions.tasks.queue_tasks.lambda_handler"
  role             = aws_iam_role.lambda_exec_role.arn
  memory_size      = var.tasks_memory
  runtime          = "python3.8"
  source_code_hash = data.archive_file.code.output_base64sha256
  timeout          = var.tasks_timeout

  layers = [aws_lambda_layer_version.layer.arn]

  environment {
    variables = local.api_environment
  }

  vpc_config {
    subnet_ids         = local.private_subnet_ids
    security_group_ids = [aws_security_group.api.id]
  }
}

resource "aws_lambda_function" "export" {
  filename         = data.archive_file.code.output_path
  function_name    = "${var.app}-${var.env}-export"
  handler          = "lambda_functions.export.lambda_handler"
  role             = aws_iam_role.lambda_exec_role.arn
  memory_size      = var.tasks_memory
  runtime          = "python3.8"
  source_code_hash = data.archive_file.code.output_base64sha256
  timeout          = var.tasks_timeout

  layers = [aws_lambda_layer_version.layer.arn]

  environment {
    variables = local.api_environment
  }

  vpc_config {
    subnet_ids         = local.private_subnet_ids
    security_group_ids = [aws_security_group.api.id]
  }
}

# ===================================
# Cloudwatch Event rule
# ===================================
resource "aws_cloudwatch_event_rule" "queue_tasks" {
  name                = "${var.app}-${var.env}-queue-tasks"
  description         = "Tasks schedule"
  schedule_expression = var.tasks_schedule
}
resource "aws_cloudwatch_event_target" "queue_tasks" {
  rule      = aws_cloudwatch_event_rule.queue_tasks.name
  target_id = "lambda"
  arn       = aws_lambda_function.queue_tasks.arn
}
resource "aws_lambda_permission" "queue_tasks" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.queue_tasks.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.queue_tasks.arn
}

# ===================================
# SQS
# ===================================
resource "aws_sqs_queue" "tasks" {
  name                       = "${var.app}-${var.env}-tasks"
  visibility_timeout_seconds = var.tasks_timeout
}

resource "aws_lambda_event_source_mapping" "tasks" {
  event_source_arn = aws_sqs_queue.tasks.arn
  enabled          = true
  function_name    = aws_lambda_function.process_tasks.arn
  batch_size       = 1
}
