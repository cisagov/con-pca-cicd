data "terraform_remote_state" "cool_pca_networking" {
  backend = "s3"

  config = {
    encrypt        = true
    bucket         = "cisa-cool-terraform-state"
    dynamodb_table = "terraform-state-lock"
    region         = "us-east-1"
    key            = "cool-pca-transitgateway-attachment/terraform.tfstate"
    role_arn       = "arn:aws:iam::210193616405:role/AccessPCATerraformBackend"
    session_name   = "pca-github-actions"
  }

  workspace = var.workspace_type
}

data "terraform_remote_state" "sharedservices_networking" {
  backend = "s3"

  config = {
    encrypt        = true
    bucket         = "cisa-cool-terraform-state"
    dynamodb_table = "terraform-state-lock"
    region         = "us-east-1"
    key            = "cool-sharedservices-networking/terraform.tfstate"
    role_arn       = "arn:aws:iam::210193616405:role/ReadSharedServicesNetworkingTerraformState"
    session_name   = "pca-github-actions"
  }

  workspace = var.workspace_type
}
