# This is a Makefile for dev and deployment commands
NAME := cpa-data-service

.PHONY: test

# target: build = build all containers
docker-build:
	docker-compose build

#target: cp - copy env into correct file
copy-env:
	echo "copy file..."
	cp deployment/env.dist .env

# target: up - Run local web server.
docker-up:
	 docker-compose up -d

# target: stop - Stop all docker containers
docker-stop:
	docker-compose stop

# target: down - Remove all docker containers
docker-down:
	docker-compose down

test:
	echo "No tests at service level ..."
