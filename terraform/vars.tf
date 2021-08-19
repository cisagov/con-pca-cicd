#=================================================
#  PROVIDER
#=================================================
variable "account_id" {
  type = string
}

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
#  COGNITO
#=================================================
variable "additional_redirect" {
  type    = string
  default = ""
}

#=================================================
#  LOGS
#=================================================
variable "log_retention_days" {
  type = number
}

#=================================================
#  LOAD BALANCING
#=================================================
variable "idle_timeout" {
  type    = number
  default = 600
}

#=================================================
#  ROUTE 53
#=================================================
variable "route53_zone_name" {
  type = string
}

#=================================================
#  DOCUMENTDB
#=================================================
variable "documentdb_cluster_size" {
  type = number
}

variable "documentdb_instance_class" {
  type = string
}

#=================================================
#  FARGATE
#=================================================
variable "cpu" {
  type = number
}

variable "memory" {
  type = number
}

variable "desired_count" {
  type = number
}

#=================================================
#  API
#=================================================
variable "api_image_repo" {
  type = string
}

variable "api_image_tag" {
  type = string
}

#=================================================
#  LANDING
#=================================================
variable "landing_subdomain" {
  type = string
}

#=================================================
#  UI
#=================================================
variable "ui_image_repo" {
  type = string
}

variable "ui_image_tag" {
  type = string
}

#=================================================
#  SES
#=================================================
variable "ses_arn" {
  type = string
}

#=================================================
#  ABOUT
#=================================================
variable "deployed_date" {
  type = string
}
