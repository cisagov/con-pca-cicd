#=================================================
#  PROVIDER
#=================================================
variable "shared_services_account_id" {
  type        = string
  description = "Account ID for DNS shared services role."
}

variable "workspace_type" {
  type = string
}

variable "account_id" {
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
  default = ["s3:*", "sqs:*", "cognito-idp:*"]
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

variable "gophish_landing_subdomain" {
  type = string
}

#=================================================
#  WEB
#=================================================
variable "web_image_repo" {
  type = string
}

variable "web_image_tag" {
  type = string
}

variable "web_cpu" {
  type = number
}

variable "web_memory" {
  type = number
}

variable "web_desired_count" {
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

variable "delay_minutes" {
  type    = string
  default = "5"
}

variable "api_desired_count" {
  type = number
}

variable "api_max_count" {
  type = number
}

variable "api_min_count" {
  type = number
}

variable "api_scale_out_count" {
  type = number
}

variable "api_scale_in_count" {
  type = number
}

variable "api_cpu" {
  type = number
}

variable "api_memory" {
  type = number
}

variable "api_gunicorn_workers" {
  type = string
}

variable "extra_bcc_emails" {
  type = string
}

variable "default_x_gophish_contact" {
  type = string
}

variable "reports_from_address" {
  type = string
}

variable "cron_minutes" {
  type = number
}

#=================================================
#  ABOUT
#=================================================
variable "deployed_date" {
  type = string
}
