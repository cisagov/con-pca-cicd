# AWS / Terrform / LocalStack

## AWS

### Installing CLI

The AWS CLI can be installed by either going to [https://aws.amazon.com/cli/](https://aws.amazon.com/cli/), or installing with pip.

```bash
pip install boto3
```

### Configuring CLI

After CLI has been installed, it has be configured with credentials. When running with localstack, only dummy credentials are necessary. The following will be asked for after running `aws configure`. These are the values that I put.

```bash
aws configure
AWS Access Key ID [****************_key]: # dummy_access_key
AWS Secret Access Key [****************_key]: # dummy_secret_key
Default region name [us-east-1]: # us-east-1
Default output format [json]: # json
```

### Python

To interact with AWS resource, the boto3 package is necessary. Documentation for boto3 can be found at [https://boto3.amazonaws.com/v1/documentation/api/latest/index.html](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html). To install boto3, run with pip.

```bash
pip install boto3
```

After boto3 has been installed, you can connect to AWS resources like this.

```python
import boto3

client = boto3.client('s3')
client.list_buckets()

resource = boto3.resource('s3')
resource.buckets.all()
```

## Terraform

The following are basic commands within terraform. When you do a make up, these commands are automatically run in a container, you do not need to run them within your own container. This is just what is happening behind the scenes.

### Tfstate

Tfstate contains the state of the resources when deployed inside a file. Locally this file is by default called "terraform.tfstate". At the moment this file is created in a named docker volume, so it can be removed and reset easily.

Eventually, this file will be stored in an S3 backend when we deploy to AWS. More information on backends in general can be found at [https://www.terraform.io/docs/backends/config.html](https://www.terraform.io/docs/backends/config.html). More information on s3 backends in particular can be found at [https://www.terraform.io/docs/backends/types/s3.html](https://www.terraform.io/docs/backends/types/s3.html)

### Init

This is the first command that needs to be run before anything else can be run. It initializes terraform and downloads the providers as definined with "provider.tf"

```bash
# Terraform Command
terraform init

# Output
Initializing the backend...

Initializing provider plugins...
- Checking for available provider plugins...
- Downloading plugin for provider "aws" (hashicorp/aws) 2.62.0...

The following providers do not have any version constraints in configuration,
so the latest version was installed.

To prevent automatic upgrades to new major versions that may contain breaking
changes, it is recommended to add version = "..." constraints to the
corresponding provider blocks in configuration, with the constraint strings
suggested below.

* provider.aws: version = "~> 2.62"
```

### Plan

If following good practice, terraform plan should be run prior to deploying resources. It will show the updates, deletions and additions that need to be made.

```bash
# Terraform Command
terraform plan

# Output
Terraform will perform the following actions:

  # aws_s3_bucket.bucket will be created
  + resource "aws_s3_bucket" "bucket" {
      + acceleration_status         = (known after apply)
      + acl                         = "private"
      + arn                         = (known after apply)
      + bucket                      = (known after apply)
      + bucket_domain_name          = (known after apply)
      + bucket_regional_domain_name = (known after apply)
      + force_destroy               = false
      + hosted_zone_id              = (known after apply)
      + id                          = (known after apply)
      + region                      = (known after apply)
      + request_payer               = (known after apply)
      + website_domain              = (known after apply)
      + website_endpoint            = (known after apply)

      + server_side_encryption_configuration {
          + rule {
              + apply_server_side_encryption_by_default {
                  + sse_algorithm = "AES256"
                }
            }
        }

      + versioning {
          + enabled    = (known after apply)
          + mfa_delete = (known after apply)
        }
    }

Plan: 1 to add, 0 to change, 0 to destroy.
```

### Apply

After terraform plan has been, and everything looks good, resources can be deployed. This command will deploy resources defined within *.tf files into AWS.

```bash
# Terraform Command
terraform apply

# Output
aws_s3_bucket.bucket: Creating...
aws_s3_bucket.bucket: Still creating... [10s elapsed]
aws_s3_bucket.bucket: Still creating... [20s elapsed]
aws_s3_bucket.bucket: Still creating... [30s elapsed]
aws_s3_bucket.bucket: Still creating... [40s elapsed]
aws_s3_bucket.bucket: Still creating... [50s elapsed]
aws_s3_bucket.bucket: Still creating... [1m0s elapsed]
aws_s3_bucket.bucket: Creation complete after 1m5s [id=con-pca-local-bucket]

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```

## LocalStack

### Testing

After resources have been brought up by terraform, you can use the api to query resources. To view the buckets that were provisioned, you can use the following command with the [AWS CLI](https://aws.amazon.com/cli/).

```bash
aws --endpoint-url=http://localhost:4566 s3 ls
```

And this is how you would do the same in Python.

```python
import boto3

s3 = boto3.client('s3', endpoint_url='http://localhost:4566')

s3.list_buckets()
```

### Services

Within the docker-compose file, certain aws services can be defined that come up when the docker container is started. To not consume unnessary memory, only those services that are necessary should be brought up. At the moment, only the main resources have been provisioned. Other resources that will be needed like Cognito, will require the pro version. For more details about localstack go to [https://github.com/localstack/localstack](https://github.com/localstack/localstack). For more details about the pro version of localstack, go to [https://localstack.cloud/#pricing](https://localstack.cloud/#pricing).
