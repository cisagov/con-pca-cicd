#=================================================
#  PROVIDER
#=================================================
github_actions_role = "arn:aws:iam::539063400056:role/ProvisionAccount"
workspace_type = "staging"
account_id = "539063400056"

#=================================================
#  CORE
#=================================================
env    = "staging"
app    = "con-pca"
region = "us-east-1"

#=================================================
#  DOCKER
#=================================================
image_url = "539063400056.dkr.ecr.us-east-1.amazonaws.com"

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
gophish_image_repo = "con-pca-gophish"
gophish_mysql_instance_class = "db.t3.micro"
gophish_mysql_storage = 20
gophish_cpu = 512
gophish_memory = 1024
gophish_count = 1
gophish_landing_subdomain = "gp.staging"

#=================================================
#  WEB
#=================================================
web_image_repo = "con-pca-web"
web_cpu = 2048
web_memory = 4096
web_desired_count = 1


#=================================================
#  API
#=================================================
api_image_repo = "con-pca-api"
delay_minutes = 5
# 1.5 days duration
yearly_minutes = "4320"
cycle_minutes = "2160"
monthly_minutes = "1080"
# 30 days duration
#yearly_minutes = "43200"
#cycle_minutes = "43200"
#monthly_minutes = "7200"
api_cpu = 2048
api_memory = 4096
api_gunicorn_workers = "12"
api_min_count = 1
api_max_count = 3
api_scale_out_count = 1
api_scale_in_count = -1
api_desired_count = 1
extra_bcc_emails = ""
default_x_gophish_contact="vulnerability@cisa.dhs.gov"
reports_from_address="reports@cyber.dhs.gov"

#=================================================
#  TASKS
#=================================================
tasks_memory = 2048
tasks_schedule = "rate(5 minutes)"
tasks_timeout = 870
