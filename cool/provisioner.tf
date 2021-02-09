# ------------------------------------------------------------------------------
# Create the IAM policy that allows all of the permissions necessary
# to provision the resources required in the assessment account.
# ------------------------------------------------------------------------------

data "aws_iam_policy_document" "policy" {
  statement {
    actions = [
      "acm:*Certificate*",
      "application-autoscaling:*Action*",
      "application-autoscaling:*Polic*",
      "application-autoscaling:*Target*",
      "autoscaling-plans:*ScalingPlan*",
      "cloudwatch:*Alarm*",
      "cloudwatch:*Dashboard*",
      "cloudwatch:*Metric*",
      "cognito-idp:Admin*",
      "cognito-idp:Confirm*",
      "cognito-idp:*Group*",
      "cognito-idp:*User*",
      "ec2:*Address*",
      "ec2:*InternetGateway*",
      "ec2:*NatGateway*",
      "ec2:*NetworkAcls*",
      "ec2:*NetworkInterface*",
      "ec2:*Route*",
      "ec2:*SecurityGroup*",
      "ec2:*Subnet*",
      "ec2:*Tags",
      "ecr:GetAuthorizationToken",
      "ecr:*Image*",
      "ecr:*Layer*",
      "ecr:*Polic*",
      "ecr:*Repositor*",
      "ecs:*Cluster*",
      "ecs:*Container*",
      "ecs:*Service*",
      "ecs:*Task*",
      "elasticloadbalancing:*Listener*",
      "elasticloadbalancing:*LoadBalancer*",
      "elasticloadbalancing:*Rule*",
      "elasticloadbalancing:Set*",
      "elasticloadbalancing:*SSL*",
      "elasticloadbalancing:*TargetGroup*",
      "events:*Event*",
      "events:*Permission*",
      "events:*Rule*",
      "events:*Target*",
      "lambda:*Concurrency*",
      "lambda:*Event*",
      "lambda:*Function*",
      "lambda:*Layer*",
      "logs:*Log*",
      "logs:*Metric*",
      "logs:*Polic*",
      "logs:*Quer*",
      "rds:*Cluster*",
      "rds:*Event*",
      "rds:*Instance*",
      "rds:*Option*",
      "rds:*Parameter*",
      "rds:*SecurityGroup*",
      "rds:*Snapshot*",
      "rds:*Subnet*",
      "route53:*HostedZone*",
      "route53:*ResourceRecord*",
      "s3:*Bucket*",
      "s3:*Object*",
      "sns:Publish",
      "sns:*Subscription*",
      "sns:Subscribe",
      "sns:Unsubscribe",
      "sns:*Topic*",
      "sqs:*Queue*",
      "sqs:*Message*",
      "sqs:*Permission*",
      "ssm:*Parameter*",
      "ssm:*Tags*",
      "sts:AssumeRole",
      "sts:GetCallerIdentity"
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
