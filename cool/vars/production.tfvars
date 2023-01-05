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
#  DOCUMENTDB
#=================================================
documentdb_instance_class      = "db.r5.xlarge"
documentdb_cluster_size        = 1
documentdb_snapshot_identifier = "january-6th"

#=================================================
#  ECS Service
#=================================================
cpu           = 2048
memory        = 4096
desired_count = 1
min_count     = 1
max_count     = 3

#=================================================
#  REPORT EMAIL ADDRESS
#=================================================
archival_email_address = "csd_vm_assessments_cyhy_pca@cisa.dhs.gov"

#=================================================
#  SCHEDULER
#=================================================
email_minutes = 5
task_minutes  = 5

#=================================================
#  WEB
#=================================================
web_image_repo = "con-pca-web"

#=================================================
#  API
#=================================================
api_image_repo = "con-pca-api"
