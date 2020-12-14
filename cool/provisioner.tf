# ------------------------------------------------------------------------------
# Create the IAM policy that allows all of the permissions necessary
# to provision the resources required in the assessment account.
# ------------------------------------------------------------------------------

data "aws_iam_policy_document" "policy" {
  statement {
    actions = [
      "acm:*",
      "application-autoscaling:*",
      "autoscaling-plans:*",
      "cloudwatch:*",
      "cognito-identity:*",
      "cognito-idp:*",
      "ec2:*",
      "ecr:*",
      "ecs:*",
      "elasticloadbalancing:*",
      "events:*",
      "iam:*",
      "lambda:*",
      "logs:*",
      "rds:*",
      "route53:*",
      "s3:*",
      "sns:*",
      "sqs:*",
      "ssm:*",
      "sts:*",
    ]

    resources = [
      "*"
    ]
  }
}

resource "aws_iam_policy" "policy" {
  description = "Policy for running terraform against account."
  name        = "${var.app}-${var.env}-github-actions"
  policy      = data.aws_iam_policy_document.policy.json
}

# ------------------------------------------------------------------------------
# Attach to the ProvisionAccount role the IAM policy that allows
# provisioning of the resources required in the assessment account.
# ------------------------------------------------------------------------------
resource "aws_iam_role_policy_attachment" "policy" {
  policy_arn = aws_iam_policy.policy.arn
  role       = var.provision_account_role_name
}
