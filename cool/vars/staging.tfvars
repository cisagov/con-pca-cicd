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
#  WEB
#=================================================
web_image_repo = "con-pca-web"

#=================================================
#  API
#=================================================
api_image_repo = "con-pca-api"
