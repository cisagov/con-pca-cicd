#! /bin/sh
terraform init
terraform plan -state "/app/state/terraform.tfstate"
terraform apply -auto-approve -var-file="local.tfvars" -state "/app/state/terraform.tfstate"
