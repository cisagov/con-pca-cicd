#=================================================
#  PROVIDER
#=================================================
workspace_type = "staging"

#=================================================
#  CORE
#=================================================
env    = "staging"
app    = "con-pca"
region = "us-east-1"

#=================================================
#  DOCUMENTDB
#=================================================
documentdb_instance_class = "db.t3.medium"
documentdb_cluster_size   = 1

#=================================================
#  ECS Service
#=================================================
cpu           = 2048
memory        = 4096
desired_count = 1
min_count     = 1
max_count     = 2

#=================================================
#  MONGO ATLAS
#=================================================
atlasorgid          = "63d4257417628664a6af2891"
mongo_type          = "ATLAS"
mongo_instance_size = "M20"

#=================================================
#  REPORT EMAIL ADDRESS
#=================================================
archival_email_address = "con.pca.reports@gmail.com"

#=================================================
#  SCHEDULER
#=================================================
email_minutes         = 2
task_minutes          = 2
failed_emails_minutes = 240

#=================================================
#  WEB
#=================================================
web_image_repo = "con-pca-web"

#=================================================
#  API
#=================================================
api_image_repo = "con-pca-api"
