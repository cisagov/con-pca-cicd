[CmdletBinding()]
param (
    [String]$AccountId = "780016325729",
    [String]$Region = "us-east-1",
    [String][Parameter(Mandatory = $true)]$Tag
)

docker build "https://github.com/cisagov/con-pca.git#develop:client" -t con-pca-web:$Tag -f prod.Dockerfile
aws ecr get-login-password --region $Region | docker login --username AWS --password-stdin "$AccountId.dkr.ecr.$Region.amazonaws.com"
docker tag "con-pca-web:$Tag" "$AccountId.dkr.ecr.$Region.amazonaws.com/con-pca-web:$Tag"
docker push "$AccountId.dkr.ecr.$Region.amazonaws.com/con-pca-web:$Tag"