#=================================================
#  PROVIDER
#=================================================
variable "github_actions_role" {
  type = string
}

#=================================================
#  PROVISION ACCOUNT
#=================================================
variable "provision_account_role_name" {
  type    = string
  default = "ProvisionAccount"
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
#  ROUTE 53
#=================================================
variable "hosted_zone_name" {
  type = string
}

#=================================================
#  COGNITO
#=================================================
variable "additional_redirect" {
  type    = string
  default = ""
}

#=================================================
#  LOAD BALANCING
#=================================================
variable "idle_timeout" {
  type    = number
  default = 600
}

#=================================================
#  LOGS
#=================================================
variable "log_retention_days" {
  type = number
}

#=================================================
#  SES
#=================================================
variable "ses_assume_role_arn" {
  type = string
}

#=================================================
#  IAM
#=================================================
variable "allowed_actions" {
  type    = list(string)
  default = ["s3:*", "sqs:*"]
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
#  BROWSERLESS
#=================================================
variable "browserless_cpu" {
  type = number
}

variable "browserless_memory" {
  type = number
}

variable "browserless_count" {
  type = number
}
