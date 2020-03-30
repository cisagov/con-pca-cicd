# This is a Makefile for dev and deployment commands
test:
	make test -C ./base/mongodb
	make test -C ./middlewares
	make test -C ./services

docker-build:
	make docker-build -C ./base/mongodb
	make docker-build -C ./services

docker-up:
	make docker-up -C ./base/mongodb
	make docker-up -C ./services

docker-stop:
	make docker-stop -C ./base/mongodb
	make docker-stop -C ./services

docker-down:
	make docker-down -C ./base/mongodb
	make docker-down -C ./services

copy-env:
	make copy-env -C ./services
