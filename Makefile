.PHONY: all help build logs loc up stop down

# make all - Default Target. Does nothing.
all:
	@echo "Project helper commands."
	@echo "For more information try 'make help'."

# target: help - Display callable targets.
help:
	@egrep "^# target:" [Mm]akefile

# target: build = build all containers
build:
	docker-compose -f ./client/docker-compose.yml build
	docker-compose -f ./controller/docker-compose.yml build
	docker-compose -f ./gophish/docker-compose.yml build

# target: up - Run GoPhish.
up:
	docker-compose -f ./client/docker-compose.yml up -d
	docker-compose -f ./controller/docker-compose.yml up -d
	docker-compose -f ./gophish/docker-compose.yml up -d

# target: stop - Stop all docker containers
stop:
	docker-compose -f ./client/docker-compose.yml stop
	docker-compose -f ./controller/docker-compose.yml stop
	docker-compose -f ./gophish/docker-compose.yml stop

# target: down - Remove all docker containers
down:
	docker-compose -f ./client/docker-compose.yml down
	docker-compose -f ./controller/docker-compose.yml down
	docker-compose -f ./gophish/docker-compose.yml down