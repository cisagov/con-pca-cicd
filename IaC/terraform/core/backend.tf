terraform {
  backend "s3" {
    bucket = "con-pca-stage-tf-backend"
    key    = "con-pca-core.tfstate"
    region = "us-east-1"
  }
}
