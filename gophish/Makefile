.PHONY: all help build logs loc up stop down

# make all - Default Target. Does nothing.
all:
	@echo "Django helper commands."
	@echo "For more information try 'make help'."

# target: help - Display callable targets.
help:
	@egrep "^# target:" [Mm]akefile

init:
	sudo chmod u+x init.sh
	echo -e "yes\nyes\nyes" | ./init.sh

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
