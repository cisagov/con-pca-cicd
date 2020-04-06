.PHONY: all test build up stop down

CURDIR = $(realpath $(dir $(firstword $(MAKEFILE_LIST))))

# Rules
# make all - Default Target. runs local-install.
all:: install

# target: create_env = creates local python env
create_env:
	cd ${CURDIR}
	virtualenv -p python3.6 env

# target: install_requirements = installs packages in vertual env
install_requirements:
	brew tap mongodb/brew
	brew install mongodb-community
	brew install rabbitmq
	(. ${CURDIR}/env/bin/activate && pip install -r services/requirements-dev.txt)

# target: install = creates local python env and installs packages
install: create_env install_requirements

# target: clean = removes local env and build
clean:
	rm -rf ${CURDIR}/build ${CURDIR}/dist ${CURDIR}/*.egg-info

# target: cleanall = runs clean and Nukes env for reinstall
cleanall:	clean
	# Nuke the env
	rm -rf ${CURDIR}/env

# target: local_services_start = run local mongodb and rabbitmq services
local_services_start:
	brew services start mongodb-community
	brew services start rabbitmq

# target: local_services_start = stop local mongodb and rabbitmq services
local_services_stop:
	brew services stop mongodb-community
	brew services stop rabbitmq

# target: run = run service in local python env
run:
	${CURDIR}/env/bin/python3 ${CURDIR}/services/lib/service.py

# target: test = run all tests
test:
	make test -C ./middlewares
	make test -C ./services

# target: build = build all containers
build:
	make docker-build -C ./services


# target: up = deploy all containers
up:
	make docker-up -C ./services

# target: stop = stop all containers
stop:
	make docker-stop -C ./services

# target: down = stop and bring down all containers
down:
	make docker-down -C ./services

# target: redeploy = bring down, rebuild and redeploy all containers
redeploy: down build up

# target: copy-env = create end files for all containers
copy-env:
	make copy-env -C ./services
