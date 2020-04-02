# CPA Data Service

This is the Database service for CPA

The stucutre is as follows:

RabbitMQ -> Service -> MongoDB

ToDo: Update Config for local and docker deployment.

## Setup

Required for install:

- [Docker](https://docs.docker.com/install/ "Docker")
- [RabbitMQ](https://www.rabbitmq.com/download.html "RabbitMQ")
- [MongoDB](https://docs.mongodb.com/manual/installation/ "MongoDB")
- [Python3+](https://www.python.org/download/releases/3.0/ "Python3+")

This dev enviorment is ment to run in a local docker enviorment.

### Local Deployment

Note: Currently this is forcused on running localy on a Mac using Python3.

< Run commands here>

### Docker Deployment

< Docker commands here >

Create your .env file
`make copy-env`

Build containers
`make docker-build`

Run data base service application locally
`make docker-up`

Stop containers
`make docker-stop`

Remove containers
`make docker-down`

## Testing

Run tests locally
`make test`
