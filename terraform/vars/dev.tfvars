#=================================================
#  CORE
#=================================================
env = "dev"
app = "con-pca"
region = "us-east-1"

#=================================================
#  COGNITO
#=================================================
additional_redirect = "http://localhost:4200"

#=================================================
#  LOGS
#=================================================
log_retention_days = 7

#=================================================
#  NETWORK
#=================================================
private_subnet_ids = [
    "subnet-0153f175feb0dfce5",
    "subnet-02f0f6199dd75238b"
]

public_subnet_ids = [
    "subnet-0a365c16b67a2b6b0",
    "subnet-0ea8f699bed93417c"
]

vpc_id = "vpc-074f7db64238a2d16"

#=================================================
#  LOAD BALANCING
#=================================================
idle_timeout = 600

#=================================================
#  ROUTE 53
#=================================================
route53_zone_name = "inltesting.xyz"

#=================================================
#  GOPHISH
#=================================================
gophish_image_repo = "780016325729.dkr.ecr.us-east-1.amazonaws.com/con-pca-gophish"
gophish_mysql_instance_class = "db.t3.micro"
gophish_mysql_storage = 20
gophish_cpu = 512
gophish_memory = 1024
gophish_count = 1
gophish_landing_subdomain = "gp.dev"

#=================================================
#  API
#=================================================
api_image_repo = "780016325729.dkr.ecr.us-east-1.amazonaws.com/con-pca-api"

delay_minutes = 5

# 30 minutes duration
# yearly_minutes = "30"
# cycle_minutes = "30"
# monthly_minutes = "15"

# 4 hours duration
#yearly_minutes = "960"
#cycle_minutes = "240"
#monthly_minutes = "80"

# 4 days duration
yearly_minutes = "5760"
cycle_minutes = "5760"
monthly_minutes = "1440"

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

#=================================================
#  DOCUMENTDB
#=================================================
documentdb_cluster_size = 1
documentdb_instance_class = "db.r5.large"

#=================================================
#  BROWSERLESS
#=================================================
browserless_cpu = 512
browserless_memory = 1024
browserless_count = 1

#=================================================
#  TASKS
#=================================================
tasks_memory = 2048
tasks_schedule = "rate(5 minutes)"
tasks_timeout = 870

#=================================================
#  WEB
#=================================================
web_image_repo = "780016325729.dkr.ecr.us-east-1.amazonaws.com/con-pca-web"
web_cpu = 2048
web_memory = 4096
web_desired_count = 1