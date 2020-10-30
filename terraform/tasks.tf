# ===================================
# Lambda Layer
# ===================================
data "archive_file" "layer" {
  type        = "zip"
  source_dir  = "${path.module}/layers/layer"
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

data "archive_file" "scikit" {
  type        = "zip"
  source_dir  = "${path.module}/layers/scikit"
  output_path = "${path.module}/output/scikit.zip"
}

resource "aws_lambda_layer_version" "scikit" {
  filename         = data.archive_file.scikit.output_path
  source_code_hash = data.archive_file.scikit.output_path
  layer_name       = "${var.app}-${var.env}-scikit"

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

resource "aws_lambda_function" "tasks" {
  filename         = data.archive_file.code.output_path
  function_name    = "${var.app}-${var.env}-tasks"
  handler          = "lambda_functions.tasks.handler.lambda_handler"
  role             = aws_iam_role.lambda_exec_role.arn
  memory_size      = var.tasks_memory
  runtime          = "python3.8"
  source_code_hash = data.archive_file.code.output_base64sha256
  timeout          = var.tasks_timeout

  layers = [
    "arn:aws:lambda:us-east-1:668099181075:layer:AWSLambda-Python38-SciPy1x:29",
    aws_lambda_layer_version.layer.arn,
    aws_lambda_layer_version.scikit.arn
  ]

  environment {
    variables = local.api_environment
  }

  vpc_config {
    subnet_ids         = var.private_subnet_ids
    security_group_ids = [aws_security_group.api.id]
  }
}

# ===================================
# Cloudwatch Event rule
# ===================================
resource "aws_cloudwatch_event_rule" "tasks" {
  name                = "${var.app}-${var.env}-tasks"
  description         = "Tasks schedule"
  schedule_expression = var.tasks_schedule
}
resource "aws_cloudwatch_event_target" "tasks" {
  rule      = aws_cloudwatch_event_rule.tasks.name
  target_id = "lambda"
  arn       = aws_lambda_function.tasks.arn
}
resource "aws_lambda_permission" "tasks" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.tasks.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.tasks.arn
}

