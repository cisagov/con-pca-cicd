# CPA Data Service

This is the Database service for CPA

The stucutre is as follows:

RabbitMQ -> Service -> MongoDB

ToDo: Update Config for local and docker deployment.

## Setup

Required for install:

<!--Please add required software information here-->

- [Docker](https://docs.docker.com/install/ "Docker")
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

#### Example

First you create a model with validator.
You can see this is `test_validators.py`

```python
from repository.models import Model
from repository.types import DateTimeType, StringType, UUIDType


class DemoModel(Model):
    """
    This is an example Model.

    This shows basic types that we will use on each model.
    """

    demo_uuid = UUIDType()
    name = StringType()
    enum_type = StringType(required=True, choices=("initial", "post", "pre", "final"))
    record_tstamp = DateTimeType(required=True)
    method_of_record_creation = StringType()
    last_updated_by = StringType(required=False, max_length=255)
    lub_timestamp = DateTimeType(required=False)
    method_of_lu = StringType(required=False)


def validate_demo(demo):
    """
    This is an example validate_demo.

    This shows basic validation for the model.
    """
    return DemoModel(demo).validate()
```

```python

import asyncio

from cpa_data_service.services.lib.service import Service
from {model_path}.test_validators import DemoModel, validate_demo

loop = asyncio.new_event_loop()
asyncio.set_event_loop(cls.loop)

your_service = Service(
            mongo_url=your_mongo_url,
            collection_name=your_collection_name,
            model=YourModel,
            model_validation=validate_yourmodel)
```

And thats it! Method calls are:

Note: This lib is asynchronous thus requires a Loop to be called from a
synchronous function.

```python
# Filter_list
loop.run_until_complete(demo_service.filter_list(parameters=parameters))
# in: {"field": "value"}
# out: [ {"field": "value"}, {"field": "value"}... ]

# Create
loop.run_until_complete(demo_service.create(to_create=to_create))
# in: to_create_object = {"field": "value"}
# out: objectID

# Get
loop.run_until_complete(demo_service.get(uuid=uuid))
# in: uuid = aaaa-111-222-3333
# out: object = {"field": "value"}

# Update
loop.run_until_complete(demo_service.update(to_update=to_update))
# in: to_update_object = {"field": "value"}
# out: objectID

# Delete
loop.run_until_complete(demo_service.delete(uuid=uuid))
# in: uuid = aaaa-111-222-3333
# out: true if delete was successful

#Count
loop.run_until_complete(demo_service.count(parameters=parameters))
# in: {"field": "value"}
# out: int: 1

```

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
Creating cpa-mongodb  ... done
```

you can then check the status of the services via `docker ps`

```shell
cpa_data_service|feature/dataservice-devdocs⚡ ⇒ docker ps
CONTAINER ID        IMAGE                            COMMAND                  CREATED             STATUS PORTS                                                                                        NAMES
<CONTAINER ID>         mongo:3.6                        "docker-entrypoint.s…"   6 minutes ago       Up 6 minutes        127.0.0.1:27017->27017/tcp                                                                   cpa-mongodb
```

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
Stopping cpa-mongodb      ... done
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
```

target: local_services_start = stop local mongodb and rabbitmq services

```shell
local_services_stop:
    brew services stop mongodb-community
```

target: run = run service in local python env

```shell
run:
    ${CURDIR}/env/bin/python3 ${CURDIR}/services/lib/service.py
```

target: test = run all tests

```shell
test:
    ${CURDIR}/env/bin/python3 ${CURDIR}/services/lib/tests.py
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
