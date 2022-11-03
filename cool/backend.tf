terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "= 4.37.0"
    }
  }

  backend "s3" {
    encrypt        = true
    bucket         = "cisa-cool-terraform-state"
    dynamodb_table = "terraform-state-lock"
    region         = "us-east-1"
    key            = "con-pca-cicd/terraform.tfstate"
    role_arn       = "arn:aws:iam::210193616405:role/AccessPCATerraformBackend"
    session_name   = "pca-github-actions"
  }
}
