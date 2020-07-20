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

variable "gophish_alb_port" {
  type = number
}

variable "landingpage_alb_port" {
    type = number
}

variable "vpc_id" {
  type = string
}

variable "health_check_interval" {
  type    = number
  default = 60
}

variable "health_check_path" {
  type    = string
  default = "/"
}

variable "health_check_codes" {
  type    = string
  default = "200,202"
}

variable "load_balancer_arn" {
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

variable "health_check_unhealthy_threshold" {
  type    = number
  default = 3
}

variable "health_check_healthy_threshold" {
  type    = number
  default = 3
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

variable "container_protocol" {
  type    = string
  default = "HTTP"
}

variable "iam_server_cert_arn" {
  type = string
}
