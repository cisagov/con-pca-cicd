.PHONY: all help build logs loc up stop down

# make all - Default Target. Does nothing.
all:
	@echo "Project helper commands."
	@echo "For more information try 'make help'."

# target: help - Display callable targets.
help:
	@egrep "^# target:" [Mm]akefile

help_win:
	Select-String "^# target:" Makefile

# target: env = generate env files
env:
	cp ./client/etc/env.dist ./client/.env
	cp ./controller/etc/env.dist ./controller/.env
	cp ./gophish/etc/env.dist ./gophish/.env

# target: build = build all containers
build:
	docker-compose -f ./client/local-docker-compose.yml build
	docker-compose -f ./client/ReportService/docker-compose.yml build
	docker-compose -f ./gophish/docker-compose.yml build
	docker-compose -f ./controller/docker-compose.yml build
	docker-compose -f ./aws/docker-compose.yml build

# target: up - Run GoPhish.
up:
	docker-compose -f ./client/local-docker-compose.yml up -d
	docker-compose -f ./controller/docker-compose.yml up -d
	docker-compose -f ./gophish/docker-compose.yml up -d
	docker-compose -f ./aws/docker-compose.yml up -d

# target: local - Run all containers required for a local environment
local:
	docker-compose -f ./client/local-docker-compose.yml up -d
	docker-compose -f ./client/ReportService/docker-compose.yml up -d
	docker-compose -f ./controller/docker-compose.yml up -d
	docker-compose -f ./gophish/docker-compose.yml up -d

# target: stop - Stop all docker containers
stop:
	docker-compose -f ./client/local-docker-compose.yml stop
	docker-compose -f ./client/ReportService/docker-compose.yml stop
	docker-compose -f ./gophish/docker-compose.yml stop
	docker-compose -f ./controller/docker-compose.yml stop
	docker-compose -f ./aws/docker-compose.yml stop

# target: down - Remove all docker containers
down:
	docker-compose -f ./client/local-docker-compose.yml down &&  \
	docker-compose -f ./client/ReportService/docker-compose.yml down || \
	docker-compose -f ./gophish/docker-compose.yml down || \
	docker-compose -f ./controller/docker-compose.yml down || \
	docker-compose -f ./aws/docker-compose.yml down
