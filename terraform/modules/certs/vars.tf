variable "namespace" {
  type = string
}

variable "stage" {
  type = string
}

variable "name" {
  type = string
}

variable "dns_names" {
  type = list(string)
}

variable "common_name" {
  type = string
}
