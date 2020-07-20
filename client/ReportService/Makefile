.PHONY: all help build logs up stop down redeploy

# make all - Default Target. Does nothing.
all:
	@echo "Node helper commands."
	@echo "For more information try 'make help'."

# target: help - Display callable targets.
help:
	@egrep "^# target:" [Mm]akefile

# target: build = build all containers
build:
	docker-compose build

# target: app logs - Runs angular logs in the terminal
logs:
	 docker attach --sig-proxy=false pca-pdf-report

# target: up - Run local web server.
up:
	 docker-compose up -d

# target: stop - Stop all docker containers
stop:
	docker-compose stop

# target: down - Remove all docker containers
down:
	docker-compose down

# target: redeploy = bring down, rebuild and redeploy all containers
redeploy: down build up
