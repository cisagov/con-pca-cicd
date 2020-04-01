# This is a Makefile for dev and deployment commands
test:
	make test -C ./middlewares
	make test -C ./services

build:
	make docker-build -C ./services

up:
	make docker-up -C ./services

stop:
	make docker-stop -C ./services

down:
	make docker-down -C ./services

copy-env:
	make copy-env -C ./services
