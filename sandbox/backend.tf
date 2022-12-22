terraform {

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "= 4.37.0"
    }
    mongodbatlas = {
      source  = "mongodb/mongodbatlas"
      version = "1.6.1"
    }
  }

  backend "s3" {
    bucket         = "inl-tf-backend"
    key            = "con-pca"
    region         = "us-east-1"
    dynamodb_table = "inl-tf-lock"
  }
}
