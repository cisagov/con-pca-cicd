#=================================================
#  PROVIDER
#=================================================
variable "account_id" {
  type = string
}

variable "workspace_type" {
  type        = string
  description = "Terraform Workspace"
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
#  MAILGUN
#=================================================
variable "mailgun_api_key" {
  type        = string
  description = "The api key for Mailgun."
}

#=================================================
#  MONGO ATLAS
#=================================================
variable "atlasorgid" {
  description = "Atlas Organization ID"
}

variable "atlas_public_key" {
  description = "The public API key for MongoDB Atlas"
}

variable "atlas_private_key" {
  description = "The private API key for MongoDB Atlas"
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
#  REPORT EMAIL ADDRESS
#=================================================
variable "archival_email_address" {
  type        = string
  description = "BCC email address for emailed reports."
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
#  MAXMIND
#=================================================
variable "maxmind_user_id" {
  type        = string
  description = "The user ID for Maxmind."
}

variable "maxmind_license_key" {
  type        = string
  description = "The license key for Maxmind."
}

#=================================================
#  ROUTE 53
#=================================================
variable "route53_zone_name" {
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
#  TASKS
#=================================================
variable "tasks_image_repo" {
  type = string
}

variable "tasks_image_tag" {
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
