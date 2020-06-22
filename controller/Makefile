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
	 docker attach --sig-proxy=false pca-api

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
	docker exec -it pca-api python manage.py shell

# target: format - Format Python code
format:
	docker exec pca-api isort --multi-line=3 --trailing-comma --force-grid-wrap=0 --use-parentheses --line-width=100 -rc .
	docker exec pca-api black -l 100 .

# target: db_load_dummy - connects to db and creates dummy-data and dumps file with id's
db_load_dummy:
	docker exec -it pca-api python scripts/create_dummy_data.py

# target: init - initializes gophish, creates tags, and creates dummy data
init:
	docker exec -it pca-api python scripts/init_gophish.py
	docker exec -it pca-api python scripts/load_tags.py
	docker exec -it pca-api python scripts/create_dummy_data.py

# target: tags - initializes tags for cpa
tags:
	docker exec -it pca-api python scripts/load_tags.py

# target: db_drop_mongo - connects to docker and drops mongo volume
db_drop_mongo:
	docker volume rm controller_mongodb

# target: coverage - runs pytests against code and generates coverage html
coverage:
	coverage run --omit *.venv*,*test* -m pytest ./src/ --disable-warnings
	coverage html

# target: cc - calculates cyclomatic complexity
cc:
	radon cc ./src/ -e "*.venv*" -s -o SCORE

# target: mi - calculates maintainability index
mi:
	radon mi ./src/ -e "*.venv*" -s

# target: hal - calculates halstead complexity metric
hal:
	radon hal ./src/ -e "*.venv*"

# target: collectstatic - collects static files to serve
collectstatic:
	docker exec -it pca-api python manage.py collectstatic

# target: build emails - build mjml files to html
build_emails:
	npm run build-emails

# target: send emails - send reports emails
send_emails:
	docker exec -it pca-api python manage.py send_reports_emails

# target: debug_ptvsd - run debugger with ptvsd
debug_ptvsd:
	docker exec -it pca-api python -m ptvsd --host 0.0.0.0 --port 5679 scripts/create_dummy_data.py
