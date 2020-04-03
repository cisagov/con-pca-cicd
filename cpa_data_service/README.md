# CPA Data Service

This is the Database service for CPA

The stucutre is as follows:

RabbitMQ -> Service -> MongoDB

ToDo: Update Config for local and docker deployment.

## Setup

Required for install:

<!--Please add required software information here-->

- [Docker](https://docs.docker.com/install/ "Docker")
- [RabbitMQ](https://www.rabbitmq.com/download.html "RabbitMQ")
- [MongoDB](https://docs.mongodb.com/manual/installation/ "MongoDB")
- [Python3+](https://www.python.org/download/releases/3.0/ "Python3+")

This dev enviorment is ment to run in a local docker enviorment.

## Additional Suggestions

Here are some additinal software to use along with develpment.
These items are not required for development.

<!--Please add addational software information here-->

- [VS Code](https://code.visualstudio.com/ "VS Code")
- [MongoDB Compass](https://www.mongodb.com/products/compass "MongoDB Compass")

VS Code is an IDE that supports pluggins to help centalize development.

MongoDB Compass is a GUI for MongoDB. This will help in visually exploring your
data.

## Local Install and Deployment

<!--Please add steps for local deployment of software information here-->

Note: Currently this is forcused on running localy on a Mac using Python3.

### Git Clone Project

Make sure you have a github account and access to the correct repo.

To install project run

```shell
git clone git@github.com:cisagov/cpa.git
cd cpa/cpa_data_service
```

Use `Makefile` to install and run `cpa_data_service` backend services.

### Mac Install

To install requirements

```shell
make install
```

This will create a vertual env and install requirments within it.

### Local Deployment

Local configuration file is located at `services/deployment/local_config.json`

When started will check for env variable `CPA_DATA_CONFIG_FILE` for file path
for config, otherwise will load from default file location.

To run locally use these steps:

```shell
make local_services_start
```

This will start local instances of rabbitmq and mongoDB services to stop them run.

```shell
make local_services_stop
```

Then to run the service use:

```shell
make run
```

the output should be something like:

```log
INFO:root:service_config {'rabbit_host': 'rabbitmq', 'mongo_uri': 'mongodb://root:rootpassword@mongodb:27017/'}
INFO:root:init database on start...
INFO:root:data inserted: 5e878b2aa0b714817253e082
INFO:root:data found: {'_id': ObjectId('5e878b2aa0b714817253e082'), 'user': 'foo', 'text': 'Long text feild for testing!', 'tags': ['one', 'two', 'three'], 'date': datetime.datetime(2020, 4, 3, 19, 14, 50, 146000)}
INFO:root:DB collection names: ['test_collection']
INFO:root:init database on finished!
INFO:pika.adapters.utils.connection_workflow:Pika version 1.1.0 connecting to ('172.28.0.3', 5672)
...
INFO:root:Strating service rabbit_client
INFO:root:server version: Database(MongoClient(host=['mongodb:27017'], document_class=dict, tz_aware=False, connect=True), 'version')
INFO:root:test db client: ['admin', 'config', 'cpa_data_dev', 'local']
INFO:root:Starting client: rabbit-client
INFO:pika.adapters.blocking_connection:Created channel=1
INFO:root:[*] Listening on queue: data_queue
INFO:root:[*] Sending on queue: db_responce. To exit press CTRL+C'
```

now the service is up and running! you can send basic messages over rabbitmq
and have it entered into the DB.

#### Example

With services up and running, run:

```log
cpa_data_service|develop⚡⇒ python3 services/lib/tests.py
[x] Sent '{'collection': 'test_collection', 'data':...
```

On the log output you will see:

```log
INFO:root:[*] Sending on queue: db_responce. To exit press CTRL+C'
 [x] {'collection': 'test_collection', 'data': {'user': 'bar', 'text': 'Long text feild for testing!', 'tags': ['one', 'two', 'three'], 'date': '2020-04-03 19:18:44.530709'}}
INFO:root:Sending to db now: {'collection': 'test_collection', 'data': {'user': 'bar', 'text': 'Long text feild for testing!', 'tags': ['one', 'two', 'three'], 'date': '2020-04-03 19:18:44.530709'}}
INFO:root:inserting into database colleciton test_collection!
INFO:root:DB success! responding to queue: {'id': '5e878c14a0b714817253e083'}
```

Success!

## Docker Install and Deployment

<!--Please add steps for docker/cloud deployment of software information here-->

To run Via Docker, first make sure you docker is running and up.

You can see what containers are up and running with `docker ps`

```shell
cpa_data_service|develop⚡ ⇒ docker ps
CONTAINER ID        IMAGE                            COMMAND                  CREATED             STATUS              PORTS
```

### Setup and Build

To create `.env` files for containers, use this command to generate them.
These files are used as configuration in deployment.

```shell
make copy-env
```

To build docker containers

```shell
make build
```

This will build docker images and track the latest changes.

Note: Make sure changes in your IDE are saved before running this command.

### Deploy to Docker

Run this make command to deploy to docker instance and then check health of
services.

```shell
make up
```

Output will be

```shell
cpa_data_service|develop⚡ ⇒ make up
make docker-up -C ./services
docker-compose up -d
Creating network "services_default" with the default driver
Creating cpa-rabbitmq ... done
Creating cpa-mongodb  ... done
Creating cpa-data-service ... done
```

you can then check the status of the services via `docker ps`

```shell
cpa_data_service|feature/dataservice-devdocs⚡ ⇒ docker ps
CONTAINER ID        IMAGE                            COMMAND                  CREATED             STATUS PORTS                                                                                        NAMES
<CONTAINER ID>        services_data-service            "python3 ./service.py"   6 minutes ago       Up 6 minutes        0.0.0.0:3000->3000/tcp                                                                       cpa-data-service
<CONTAINER ID>         rabbitmq:3.6-management-alpine   "docker-entrypoint.s…"   6 minutes ago       Up 6 minutes        4369/tcp, 5671/tcp, 0.0.0.0:5672->5672/tcp, 15671/tcp, 25672/tcp, 0.0.0.0:15672->15672/tcp   cpa-rabbitmq
<CONTAINER ID>         mongo:3.6                        "docker-entrypoint.s…"   6 minutes ago       Up 6 minutes        127.0.0.1:27017->27017/tcp                                                                   cpa-mongodb
```

Note: `services_data-service` might restart a few times waiting for rabbitmq
service to start. currently this service depends on rabbitmq to be up and
connected before running.

Success! all services are running.

### Redeploy

While containters are running and re redeploy new changes, you can use

```shell
make redeploy
```

This will stop, rebuild and deploy all containers again.

### Docker Teardown

To stop all containers, use this command to stop and takedown.

```shell
make down
```

This will look like:

```shell
cpa_data_service|develop⚡ ⇒ make down
make docker-down -C ./services
docker-compose down
Stopping cpa-data-service ... done
Stopping cpa-rabbitmq     ... done
Stopping cpa-mongodb      ... done
Removing cpa-data-service ... done
Removing cpa-rabbitmq     ... done
Removing cpa-mongodb      ... done
Removing network services_default
```

Once that finishes, all docker containers used by this serives will be stopped.

Notice: Messeges left in rabbitMQ service will be lost but MongoDB data will
persistent.

## Makefile

The following are the current Makefile Rules and commands.

Makefile Rules:

make all - Default Target. runs local-install.

```shell
all:: install
```

target: create_env = creates local python env

```shell
create_env:
    cd ${CURDIR}
    virtualenv -p python3.6 env
```

target: install_requirements = installs packages in vertual env

```shell
install_requirements:
    brew tap mongodb/brew
    brew install mongodb-community
    brew install rabbitmq
    (. ${CURDIR}/env/bin/activate && pip install -r services/requirements-dev.txt)
```

target: install = creates local python env and installs packages

```shell
install: create_env install_requirements
```

target: clean = removes local env and build

```shell
clean:
    rm -rf ${CURDIR}/build ${CURDIR}/dist ${CURDIR}/*.egg-info
```

target: cleanall = runs clean and Nukes env for reinstall

```shell
cleanall:    clean
    # Nuke the env
    rm -rf ${CURDIR}/env
```

target: local_services_start = run local mongodb and rabbitmq services

```shell
local_services_start:
    brew services start mongodb-community
    brew services start rabbitmq
```

target: local_services_start = stop local mongodb and rabbitmq services

```shell
local_services_stop:
    brew services stop mongodb-community
    brew services stop rabbitmq
```

target: run = run service in local python env

```shell
run:
    ${CURDIR}/env/bin/python3 ${CURDIR}/services/lib/service.py
```

target: test = run all tests

```shell
test:
    make test -C ./middlewares
    make test -C ./services
```

target: build = build all containers

```shell
build:
    make docker-build -C ./services
```

target: up = deploy all containers

```shell
up:
    make docker-up -C ./services
```

target: stop = stop all containers

```shell
stop:
    make docker-stop -C ./services
```

target: down = stop and bring down all containers

```shell
down:
    make docker-down -C ./services
```

target: redeploy = bring down, rebuild and redeploy all containers

```shell
redeploy: down build up
```

target: copy-env = create end files for all containers

```shell
copy-env:
    make copy-env -C ./services
```

## Testing

<!--Please add steps for testing of software information here-->

Run tests locally
`make test`
