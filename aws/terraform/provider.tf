provider "aws" {
    access_key                  = "mock_access_key"
    secret_key                  = "mock_secret_key"
    region                      = "us-east-1"
    s3_force_path_style         = true
    skip_credentials_validation = true
    skip_metadata_api_check     = true
    skip_requesting_account_id  = true

    endpoints {
        apigateway     = "http://pca-localstack:4566"
        cloudformation = "http://pca-localstack:4566"
        cloudwatch     = "http://pca-localstack:4566"
        dynamodb       = "http://pca-localstack:4566"
        es             = "http://pca-localstack:4566"
        firehose       = "http://pca-localstack:4566"
        iam            = "http://pca-localstack:4566"
        kinesis        = "http://pca-localstack:4566"
        lambda         = "http://pca-localstack:4566"
        route53        = "http://pca-localstack:4566"
        redshift       = "http://pca-localstack:4566"
        s3             = "http://pca-localstack:4566"
        secretsmanager = "http://pca-localstack:4566"
        ses            = "http://pca-localstack:4566"
        sns            = "http://pca-localstack:4566"
        sqs            = "http://pca-localstack:4566"
        ssm            = "http://pca-localstack:4566"
        stepfunctions  = "http://pca-localstack:4566"
        sts            = "http://pca-localstack:4566"
    }
}