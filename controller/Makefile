.PHONY: all help build logs loc up stop down

# make all - Default Target. Does nothing.
all:
	@echo "Django helper commands."
	@echo "For more information try 'make help'."

# target: help - Display callable targets.
help:
	@egrep "^# target:" [Mm]akefile

# target: build = build all containers
build:
	docker-compose build

# target: app logs - Runs django logs in the terminal
logs:
	 docker attach --sig-proxy=false cpa-api

# target: loc - Count lines of code.
loc:
	 loc src

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

# target: shell - django shell within container
shell:
	docker exec -it cpa-api python manage.py shell

# target: format - Format Python code
format:
	docker exec cpa-api isort --multi-line=3 --trailing-comma --force-grid-wrap=0 --use-parentheses --line-width=100 -rc .
	docker exec cpa-api black -l 100 .

# target: db_load_dummy - connects to db and creates dummy-data and dumps file with id's
db_load_dummy:
	python scripts/create_dummy_data.py

# target: db_drop_mongo - connects to docker and drops mongo volume
db_drop_mongo:
	docker volume rm controller_mongodb
