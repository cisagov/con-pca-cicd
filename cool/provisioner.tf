# ------------------------------------------------------------------------------
# Create the IAM policy that allows all of the permissions necessary
# to provision the resources required in the assessment account.
# ------------------------------------------------------------------------------

data "aws_iam_policy_document" "policy" {
  statement {
    actions = [
      "acm:DeleteCertificate",
      "acm:DescribeCertificate",
      "acm:RequestCertificate",
      "acm:RemoveTagsFromCertificate",
      "acm:GetCertificate",
      "acm:UpdateCertificateOptions",
      "acm:AddTagsToCertificate",
      "acm:ListCertificates",
      "acm:ListTagsForCertificate",
      "application-autoscaling:*",
      "autoscaling-plans:*",
      "cloudwatch:*",
      "cognito-idp:*",
      "ec2:DeleteSubnet",
      "ec2:ReplaceRouteTableAssociation",
      "ec2:AttachInternetGateway",
      "ec2:DescribePlacementGroups",
      "ec2:ReplaceRoute",
      "ec2:AssociateRouteTable",
      "ec2:DeleteRouteTable",
      "ec2:DescribeInternetGateways",
      "ec2:CreateRoute",
      "ec2:CreateInternetGateway",
      "ec2:AssociateTransitGatewayRouteTable",
      "ec2:DeleteInternetGateway",
      "ec2:DescribeNetworkInterfacePermissions",
      "ec2:UnassignPrivateIpAddresses",
      "ec2:DescribeNetworkAcls",
      "ec2:DescribeRouteTables",
      "ec2:CreateTags",
      "ec2:CreateRouteTable",
      "ec2:DeleteNetworkInterface",
      "ec2:AssignPrivateIpAddresses",
      "ec2:DisassociateRouteTable",
      "ec2:CreateNetworkInterface",
      "ec2:DescribeTransitGatewayAttachments",
      "ec2:AssociateSubnetCidrBlock",
      "ec2:DeleteNatGateway",
      "ec2:CreateSubnet",
      "ec2:DescribeSubnets",
      "ec2:DisassociateAddress",
      "ec2:DeleteTags",
      "ec2:CreateNatGateway",
      "ec2:DescribeRegions",
      "ec2:DescribeTransitGateways",
      "ec2:DescribeVpcAttribute",
      "ec2:ModifySubnetAttribute",
      "ec2:DescribeNetworkInterfaces",
      "ec2:DescribeTransitGatewayRouteTables",
      "ec2:DescribeAvailabilityZones",
      "ec2:DescribeNetworkInterfaceAttribute",
      "ec2:CreateSecurityGroup",
      "ec2:CreateNetworkAcl",
      "ec2:DeleteNetworkAcl",
      "ec2:GetTransitGatewayRouteTableAssociations",
      "ec2:ReleaseAddress",
      "ec2:DeleteRoute",
      "ec2:DescribeNatGateways",
      "ec2:AllocateAddress",
      "ec2:DescribeSecurityGroups",
      "ec2:DescribeSecurityGroupReferences",
      "ec2:DescribeVpcs",
      "ec2:DeleteSecurityGroup",
      "ec2:AttachNetworkInterface",
      "ec2:DescribeTransitGatewayVpcAttachments",
      "ecr:*",
      "ecs:*",
      "elasticloadbalancing:*",
      "events:*",
      "lambda:*",
      "logs:*",
      "rds:*",
      "route53:*",
      "s3:*",
      "sns:*",
      "sqs:*",
      "ssm:PutParameter",
      "ssm:DeleteParameter",
      "ssm:DescribeParameters",
      "ssm:RemoveTagsFromResource",
      "ssm:GetParameterHistory",
      "ssm:AddTagsToResource",
      "ssm:ListTagsForResource",
      "ssm:GetParametersByPath",
      "ssm:GetParameters",
      "ssm:GetParameter",
      "ssm:DeleteParameters",
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
