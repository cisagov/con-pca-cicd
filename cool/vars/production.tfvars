#=================================================
#  PROVIDER
#=================================================
workspace_type = "production"

#=================================================
#  CORE
#=================================================
env    = "prod"
app    = "con-pca"
region = "us-east-1"

#=================================================
#  ROUTE 53
#=================================================
hosted_zone_name = "con-pca.cool.cyber.dhs.gov"

#=================================================
#  LOGS
#=================================================
log_retention_days = 7

#=================================================
#  LOAD BALANCING
#=================================================
idle_timeout = 600

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
gophish_image_repo           = "con-pca-gophish"
gophish_mysql_instance_class = "db.t3.micro"
gophish_mysql_storage        = 20
gophish_cpu                  = 512
gophish_memory               = 1024
gophish_count                = 1
gophish_landing_subdomain    = "gp.pr"

#=================================================
#  WEB
#=================================================
web_image_repo    = "con-pca-web"
web_cpu           = 2048
web_memory        = 4096
web_desired_count = 1


#=================================================
#  API
#=================================================
api_image_repo            = "con-pca-api"
delay_minutes             = 5
api_cpu                   = 2048
api_memory                = 4096
api_gunicorn_workers      = "12"
api_min_count             = 1
api_max_count             = 3
api_scale_out_count       = 1
api_scale_in_count        = -1
api_desired_count         = 1
extra_bcc_emails          = ""
default_x_gophish_contact = "vulnerability@cisa.dhs.gov"
reports_from_address      = "reports@cyber.dhs.gov"

#=================================================
#  TASKS
#=================================================
tasks_memory   = 4096
tasks_schedule = "rate(5 minutes)"
tasks_timeout  = 900
