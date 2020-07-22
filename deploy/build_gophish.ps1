[CmdletBinding()]
param (
    [String]$AccountId = "780016325729",
    [String]$Region = "us-east-1",
    [String][Parameter(Mandatory = $true)]$Tag
)

docker build "https://github.com/cisagov/con-pca.git#develop:gophish/etc/gophish" -t con-pca-gophish:$Tag
aws ecr get-login-password --region $Region | docker login --username AWS --password-stdin "$AccountId.dkr.ecr.$Region.amazonaws.com"
docker tag "con-pca-gophish:$Tag" "$AccountId.dkr.ecr.$Region.amazonaws.com/con-pca-gophish:$Tag"
docker push "$AccountId.dkr.ecr.$Region.amazonaws.com/con-pca-gophish:$Tag"