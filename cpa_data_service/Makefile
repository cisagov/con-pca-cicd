# This is a Makefile for dev and deployment commands
test:
	make test -C ./base
	make test -C ./middlewares
	make test -C ./services

docker-up:
	make docker-up -C ./base

docker-stop:
	make docker-stop -C ./base

docker-down:
	make docker-down -C ./base
