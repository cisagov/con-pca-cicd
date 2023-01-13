#=================================================
#  COGNITO
#=================================================
additional_redirect = "http://localhost:4200"

#=================================================
#  CORE
#=================================================
env    = "dev"
app    = "pca"
region = "us-east-1"

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
#  REPORT EMAIL ADDRESS
#=================================================
archival_email_address = "con.pca.reports@gmail.com"

#=================================================
#  LOGS
#=================================================
log_retention_days = 7

#=================================================
#  LOAD BALANCING
#=================================================
idle_timeout = 600

#=================================================
#  ROUTE 53
#=================================================
route53_zone_name = "inltesting.xyz"

#=================================================
#  DOCUMENTDB
#=================================================
documentdb_cluster_size   = 1
documentdb_instance_class = "db.t3.medium"

#=================================================
#  FARGATE
#=================================================
cpu           = 2048
memory        = 4096
desired_count = 1

#=================================================
#  MONGO ATLAS
#=================================================
atlasorgid  = "639b5119bc6ecf0c5fde627e"
atlasprojid = "63c1b65ceeaf9971545da035"

#=================================================
#  API
#=================================================
api_image_repo    = "con-pca-api"
landing_subdomain = "gp.dev"

#=================================================
#  UI
#=================================================
ui_image_repo = "con-pca-web"
