#=================================================
#  CORE
#=================================================
env = "dev"
app = "con-pca"
region = "us-east-1"

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