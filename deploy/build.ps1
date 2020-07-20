$account_id = "780016325729"
$region = "us-east-1"
$version = "1.0"

# Build docker images
docker build "https://github.com/cisagov/con-pca.git#develop:client" -t con-pca-web:$version -f prod.Dockerfile
docker build "https://github.com/cisagov/con-pca.git#develop:gophish/etc/gophish" -t con-pca-gophish:$version
docker build "https://github.com/cisagov/con-pca.git#develop:controller/" -t con-pca-api:$version -f etc/Dockerfile

# Tag Docker Images for ECR
aws ecr get-login-password --region $region | docker login --username AWS --password-stdin "$account_id.dkr.ecr.$region.amazonaws.com"
docker tag "con-pca-web:$version" "$account_id.dkr.ecr.$region.amazonaws.com/con-pca-web:$version"
docker tag "con-pca-gophish:$version" "$account_id.dkr.ecr.$region.amazonaws.com/con-pca-gophish:$version"
docker tag "con-pca-api:$version" "$account_id.dkr.ecr.$region.amazonaws.com/con-pca-api:$version"

# Push Docker images to ECR
docker push "$account_id.dkr.ecr.$region.amazonaws.com/con-pca-web:$version"
docker push "$account_id.dkr.ecr.$region.amazonaws.com/con-pca-gophish:$version"
docker push "$account_id.dkr.ecr.$region.amazonaws.com/con-pca-api:$version"