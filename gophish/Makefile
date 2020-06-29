.PHONY: all help build logs loc up stop down

# make all - Default Target. Does nothing.
all:
	@echo "Helper commands."
	@echo "For more information try 'make help'."

# target: help - Display callable targets.
help:
	@egrep "^# target:" [Mm]akefile

# target: build = build all containers
build:
	docker-compose build

# target: up - Run GoPhish.
up:
	 docker-compose up -d

# target: stop - Stop all docker containers
stop:
	docker-compose stop

# target: down - Remove all docker containers
down:
	docker-compose down

# target: app logs - Runs gophish logs in the terminal
logs:
	 docker attach --sig-proxy=false pca-gophish
