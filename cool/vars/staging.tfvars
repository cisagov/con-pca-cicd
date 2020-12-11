#=================================================
#  PROVIDER
#=================================================
github_actions_role = "arn:aws:iam::539063400056:role/ProvisionAccount"

#=================================================
#  CORE
#=================================================
env    = "staging"
app    = "con-pca"
region = "us-east-1"

#=================================================
#  ROUTE 53
#=================================================
hosted_zone_name = "con-pca.staging.cool.cyber.dhs.gov"

#=================================================
#  LOGS
#=================================================
log_retention_days = 7

#=================================================
#  LOAD BALANCING
#=================================================
idle_timeout = 600

#=================================================
#  SES
#=================================================
ses_assume_role_arn = "arn:aws:iam::246048611598:role/SesSendEmail-cyber.dhs.gov"

#=================================================
#  IAM
#=================================================
allowed_actions = ["s3:*", "sqs:*"]

#=================================================
#  DOCUMENTDB
#=================================================
documentdb_cluster_size   = 1
documentdb_instance_class = "db.r5.large"

#=================================================
#  BROWSERLESS
#=================================================
browserless_cpu    = 512
browserless_memory = 1024
browserless_count  = 1

#=================================================
#  GOPHISH
#=================================================
gophish_image_repo = "539063400056.dkr.ecr.us-east-1.amazonaws.com/con-pca-gophish"
gophish_mysql_instance_class = "db.t3.micro"
gophish_mysql_storage = 20
gophish_cpu = 512
gophish_memory = 1024
gophish_count = 1
