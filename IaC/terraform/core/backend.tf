terraform {
  backend "s3" {
    bucket         = "con-pca-terraform"
    key            = "tfstate/con-pca-core.tfstate"
    region         = "us-east-1"
    dynamodb_table = "con-pca-tf-lock"
  }
}
