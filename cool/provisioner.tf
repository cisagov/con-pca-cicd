# ------------------------------------------------------------------------------
# Create the IAM policy that allows all of the permissions necessary
# to provision the resources required in this account.
# ------------------------------------------------------------------------------
data "aws_iam_policy_document" "policy" {
  statement {
    actions = [
      "acm:*",
      "application-autoscaling:*",
      "cloudwatch:*",
      "cognito-idp:*",
      "ec2:*",
      "ecr:*",
      "ecs:*",
      "elasticloadbalancing:*",
      "events:*",
      "logs:*",
      "rds:*",
      "route53:*",
      "s3:*",
      "sns:*",
      "ssm:*",
      "sts:*",
    ]

    resources = [
      "*"
    ]
  }
}

resource "aws_iam_policy" "policy" {
  description = "Provisions Resources for Con-PCA"
  name        = "${var.app}-${var.env}-provision-"
  policy      = data.aws_iam_policy_document.policy.json
}

# ------------------------------------------------------------------------------
# Attach to the ProvisionAccount role the IAM policy that allows
# provisioning of the resources required.
# ------------------------------------------------------------------------------
resource "aws_iam_role_policy_attachment" "policy" {
  policy_arn = aws_iam_policy.policy.arn
  role       = var.provision_account_role_name
}
