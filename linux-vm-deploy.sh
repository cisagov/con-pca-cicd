cd client
make build_prod
make up_prod

cd ../controller
make build
make up


cd ../aws
make build
make up