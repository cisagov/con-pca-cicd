terraform {
  backend "s3" {
    bucket         = "inl-tf-backend"
    key            = "con-pca.tfstate"
    region         = "us-east-1"
    dynamodb_table = "inl-tf-lock"
  }
}
