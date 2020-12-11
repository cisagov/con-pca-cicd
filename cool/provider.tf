provider "aws" {
  region = "us-east-1"

  assume_role {
    role_arn     = var.github_actions_role
    session_name = "pca-github-actions"
  }
}
