#! /bin/sh
cp providers/$ENV.provider.tf provider.tf
terraform init
terraform plan -state "/app/state/terraform.tfstate"
terraform apply -auto-approve -var-file="vars/$ENV.tfvars" -state "/app/state/terraform.tfstate"
