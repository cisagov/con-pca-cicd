#=================================================
#  PROVIDER
#=================================================
variable "shared_services_account_id" {
  type        = string
  description = "Account ID for DNS shared services role."
}

variable "workspace_type" {
  type        = string
  description = "Terraform Workspace"
}

variable "account_id" {
  type        = string
  description = "AWS Account ID"
}

#=================================================
#  PROVISION ACCOUNT
#=================================================
variable "provision_account_role_name" {
  type        = string
  default     = "ProvisionAccount"
  description = "Role name for provision account."
}

#=================================================
#  CORE
#=================================================
variable "env" {
  type        = string
  description = "Environment deploying to."
}

variable "app" {
  type        = string
  description = "Name of application."
}

variable "region" {
  type        = string
  description = "AWS region deploying to."
}

#=================================================
#  ROUTE 53
#=================================================
variable "hosted_zone_name" {
  type        = string
  description = "Name of hosted zone for application route53."
}

#=================================================
#  SES
#=================================================
variable "ses_arn" {
  type        = string
  description = "The role to assume for sending reports via SES."
}

#=================================================
#  DOCUMENTDB
#=================================================
variable "documentdb_instance_class" {
  type        = string
  description = "Instance class for DocumentDB."
}

variable "documentdb_cluster_size" {
  type        = string
  description = "Cluster size for document db."
}

variable "documentdb_snapshot_identifier" {
  type        = string
  description = "Snapshot to create documentdb cluster off of."
  default     = ""
}

#=================================================
#  ECS Service
#=================================================
variable "cpu" {
  type        = number
  description = "Desired CPU for application."
}

variable "memory" {
  type        = number
  description = "Desired memory for applicaiton."
}

variable "desired_count" {
  type        = number
  description = "Desired count to launch application with."
}

variable "min_count" {
  type        = number
  description = "Minimum number of ECS tasks to have running at a time."
}

variable "max_count" {
  type        = number
  description = "Maximum number of ECS tasks to have running at a time."
}

#=================================================
#  WEB
#=================================================
variable "web_image_repo" {
  type        = string
  description = "The name of the Github repo for the web application."
}

variable "web_image_tag" {
  type        = string
  description = "The tag for the web image build."
}

#=================================================
#  API
#=================================================
variable "api_image_repo" {
  type        = string
  description = "The name of the Github repo for the api application."
}

variable "api_image_tag" {
  type        = string
  description = "The tag for the api image build."
}

variable "reports_from_address" {
  type        = string
  description = "The email address to receive reports from."
}


#=================================================
#  MAILGUN
#=================================================
variable "mailgun_api_key" {
  type        = string
  description = "The api key for Mailgun."
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
#  ABOUT
#=================================================
variable "deployed_date" {
  type        = string
  description = "Date of latest deployment."
}
