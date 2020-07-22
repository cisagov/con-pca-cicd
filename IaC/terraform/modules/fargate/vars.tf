variable "namespace" {
  type = string
}

variable "stage" {
  type = string
}

variable "name" {
  type = string
}

variable "container_definition" {
  type = string
}

variable "container_name" {
  type = string
}

variable "container_port" {
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

variable "load_balancer_port" {
  type = number
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

variable "container_protocol" {
  type    = string
  default = "HTTP"
}

variable "iam_server_cert_arn" {
  type = string
}
