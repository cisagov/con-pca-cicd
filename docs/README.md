# Architecture

## CloudFormation

Cloudformation is used to deploy the base infrastructure to allow terraform and deployments to work.

* Terraform S3 Backend
* ECR Repos for builds

This is a better option than going and manually creating these resources.

## Terraform

Terraform is used for the deployments of all other resources.

### Core

The core resources under terraform deploys the base networking infrastructure. This includes - VPC, Subnets, Load Balancers, Internet Gateways, etc.

### API

This deploys the api fargate service. Includes a DocumentDB database. This service is publicly available and is secured behind Cognito.

### Gophish

This deploys the gophish fargate service. Includes a MySQL RDS database. This service is also publicly available. Secured with a strong username/password that can be retrieved from AWS SSM.

### Web

This deploys the web fargate service. This service is publicly available and is secured behind Cognito.

### Reports

This deploys the reports fargate service. This service is an internal service on the private subnet. Only the API sends requests to it. It has access through the internet gateway and NAT to produce reports from the Angular website.

### Modules

There are several modules that have been produced to ease the ability of creating these fargate services. The modules include:

* Certs

Produces self-signed certificates and uploads to IAM. This is a temporary solution until this app has a domain and certificates can be uploaded to ACM.

* Container Definition

Create a container definition. Utilizes github.com/cloudposse/terraform-aws-ecs-container-definition with some additional app-specific settings.

* Fargate

Creates a fargate service behind an application load balancer.

* Gophish

Deploys gophish behind an application load balancer to Fargate.
