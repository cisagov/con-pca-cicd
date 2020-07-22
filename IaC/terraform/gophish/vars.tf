variable "env" {
  type = string
}

variable "app" {
  type    = string
  default = "con-pca"
}

variable "region" {
  type    = string
  default = "us-east-1"
}

variable "image_repo" {
  type    = string
  default = "780016325729.dkr.ecr.us-east-1.amazonaws.com/con-pca-gophish"
}

variable "image_tag" {
  type = string
}

variable "mysql_instance_class" {
  type    = string
  default = "db.t3.micro"
}

variable "mysql_storage" {
  type    = number
  default = 20
}


