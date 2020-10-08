#=================================================
#  CORE
#=================================================
variable "env" {
  type = string
}

variable "app" {
  type = string
}

variable "region" {
  type = string
}

#=================================================
#  LOGS
#=================================================
variable "log_retention_days" {
  type = number
}

#=================================================
#  NETWORK
#=================================================
variable "vpc_id" {
  type = string
}

variable "private_subnet_ids" {
  type = list(string)
}

variable "public_subnet_ids" {
  type = list(string)
}

#=================================================
#  ROUTE 53
#=================================================
variable "route53_zone_name" {
  type = string
}

#=================================================
#  GOPHISH
#=================================================
variable "gophish_image_repo" {
  type = string
}

variable "gophish_image_tag" {
  type = string
}

variable "gophish_mysql_instance_class" {
  type = string
}

variable "gophish_mysql_storage" {
  type = number
}

variable "gophish_cpu" {
  type = number
}

variable "gophish_memory" {
  type = number
}

variable "gophish_count" {
  type = number
}
