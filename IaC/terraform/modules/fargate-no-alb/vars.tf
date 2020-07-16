variable "namespace" {
  type = string
}

variable "stage" {
  type = string
}

variable "name" {
  type = string
}

variable "log_retention" {
  type    = number
  default = 7
}

variable "container_port" {
  type = number
}

variable "vpc_id" {
  type = string
}

variable "container_image" {
  type = string
}

variable "aws_region" {
  type = string
}

variable "environment" {
  type    = map(string)
  default = {}
}

variable "secrets" {
  type    = map(string)
  default = {}
}

variable "desired_count" {
  type    = number
  default = 1
}

variable "subnet_ids" {
  type = list(string)
}


variable "security_group_ids" {
  type = list(string)
}

variable "memory" {
  type = number
}

variable "cpu" {
  type = number
}

variable "entrypoint" {
  type    = list(string)
  default = null
}
