# CPA Controller

## Setup

Required for install:

<!--Please add required software information here-->

- [Docker](https://docs.docker.com/install/ "Docker")
- [MongoDB](https://docs.mongodb.com/manual/installation/ "MongoDB")
- [Python3+](https://www.python.org/download/releases/3.0/ "Python3+")

## Additional Suggestions

Here are some additional software to use along with develpment.
These items are not required for development.

<!--Please add addational software information here-->

- [VS Code](https://code.visualstudio.com/ "VS Code")
- [MongoDB Compass](https://www.mongodb.com/products/compass "MongoDB Compass")

VS Code is an IDE that supports pluggins to help centalize development.

MongoDB Compass is a GUI for MongoDB. This will help in visually exploring your
data.

## Local Install and Deployment

<!--Please add steps for local deployment of software information here-->

Note: Currently this is forcused on running locally on a Mac using Python3.

### Git Clone Project

Make sure you have a github account and access to the correct repo.

To install project run

```shell
git clone git@github.com:cisagov/cpa.git
cd cpa/controller
```

Use `Makefile` to install and run `controller` services.

### Setup and Build

To create `.env` files for containers, use this command to generate them.
These files are used as configuration in deployment.

Create your .env file

- `cp etc/env.dist .env`

Build containers

- `make build`

Run your web application locally

- `make up`

Run Django logs in the terminal

- `make logs`

Stop containers

- `make stop`

Remove containers

- `make down`

Access Django shell

- `make shell`

### To access the Django API

Django base app located at [localhost:8000](http://localhost:8000)

### To access the RabbitMQ dashboard

RabbitMQ management dashboard located at [localhost:15672](http://localhost:15672)

## Api Usage

To run the containers, use:
- `make up`

Your output will look like:

```shell
-> % make up
docker-compose up -d
Creating network "controller_default" with the default driver
Creating cpa-rabbitmq ... done
Creating cpa-mongodb  ... done
Creating cpa-worker   ... done
Creating cpa-beat     ... done
Creating cpa-api      ... done
```

Dev Access

You can use these endpoints to debug and develop, suggested access:

- [curl](https://curl.haxx.se/docs/manpage.html)

- [PostMan](https://www.postman.com/)

### API URLS

The current api url endpoints are:

| URL | ACTIONS |
| ----------- | ----------- |
| <host:port>/api/v1/subscriptions/ | [GET, POST] |
| <host:port>/api/v1/subscription/<subscription_uuid> | [GET] |
| <host:port>/api/v1/templates/ | [GET, POST] |
| <host:port>/api/v1/template/<template_uuid> | [GET] |
| <host:port>/api/v1/targets/ | [GET, POST] |
| <host:port>/api/v1/target/<target_uuid> | [GET] |

## Examples

The following are examples of URL calls.

When running locally, host:port = `http://localhost:8000/api/v1/subscriptions/`

### GET

```shell
-> % curl -i -H "Accept: application/json" -H "Content-Type: application/json" http://localhost:8000/api/v1/subscriptions/
HTTP/1.1 200 OK
Date: Tue, 14 Apr 2020 17:25:34 GMT
Server: WSGIServer/0.2 CPython/3.8.2
Content-Type: application/json
Allow: GET, POST, HEAD, OPTIONS
X-Frame-Options: DENY
Content-Length: 2859
X-Content-Type-Options: nosniff

[{"subscription_uuid":"0cb84ded-a86d-4332-932c-d9db9815ff20","organziation":"Some Company.1com", ...} ....]
```

Example JSON for GET Query:

```json
{
  "organization": "Some Company.1com"
}
```

This will query for objects with `organization` = `Some Company.1com`

### POST

```shell
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{
    "customer_uuid":  "0bd5b1c8-3f9c-482e-afe5-c9f865f890a1",
     "organization": "Some Company.1com",
     "start_date":  "2020-04-10T09:30:25",
     "end_date": "2020-04-20T00:00:00",
     "report_count": 3,
     "first_report_timestamp": "2020-04-20T00:00:00",
     "primary_contact": {
        "name": "phill",
        "email": "phill@example.com"
     },
     "additional_contact_list": [{
        "name": "bob",
        "email": "foo.bar@example.com"
     }, {
        "name": "bill",
        "email": "bill.dolla@example.com"
     }],
     "status": "Running",
     "target_email_list": [{
        "target_uuid": "0bd5b1c8-3f9c-482e-afe5-c9f865f890a1",
        "status": "sent",
        "sent_date": "2020-04-13T09:30:25"
     }, {
        "target_uuid": "0bd5b1c8-3f9c-482e-afe5-c9f865f890a1",
        "status": "sent",
        "sent_date": "2020-04-13T09:30:25"
     }],
     "templates_selected": [
        "0bd5b1c8-3f9c-482e-afe5-c9f865f890a1"
        ],
     "click_list": [{
         "source_ip": "127.1.1.12",
         "timestamp": "2020-04-13T09:30:25",
         "target_uuid": "0bd5b1c8-3f9c-482e-afe5-c9f865f890a1"
      }],
     "active": "True"}' \
  http://localhost:8000/api/v1/subscriptions/

  {
    "subscription_uuid": "cb63e7c9-2b1d-494f-b3ca-3c942bbcaaa1"
}
```

Example JSON for POST:

```json
{
   "customer_uuid":  "0bd5b1c8-3f9c-482e-afe5-c9f865f890a1",
   "organization": "Some Company.1com",
   "start_date":  "2020-04-10T09:30:25",
   "end_date": "2020-04-20T00:00:00",
   "report_count": 3,
   "first_report_timestamp": "2020-04-20T00:00:00",
   "primary_contact": {
      "name": "phill",
      "email": "phill@example.com"
   },
   "additional_contact_list": [{
      "name": "bob",
      "email": "foo.bar@example.com"
   }, {
      "name": "bill",
      "email": "bill.dolla@example.com"
   }],
   "status": "Running",
   "target_email_list": [{
      "target_uuid": "0bd5b1c8-3f9c-482e-afe5-c9f865f890a1",
      "status": "sent",
      "sent_date": "2020-04-13T09:30:25"
   },
   {
      "target_uuid": "0bd5b1c8-3f9c-482e-afe5-c9f865f890a1",
      "status": "sent",
      "sent_date": "2020-04-13T09:30:25"
   }],
   "templates_selected": [
      "0bd5b1c8-3f9c-482e-afe5-c9f865f890a1"
      ],

   "click_list": [
      {
         "source_ip": "123.12.12.1",
         "timestamp": "2020-04-13T09:30:25",
         "target_uuid": "0bd5b1c8-3f9c-482e-afe5-c9f865f890a1"
      }],
   "active": "True"
}
```

## Troubleshooting

### Know Issues

When running and calling api:

`Unauthorized`

This is due to the DB not having the correct creds.

1.) check `.env`

```shell
....

# MongoDB
DB_HOST=mongodb
DB_PORT=27017
DB_PW=rootpassword
DB_USER=root

# DB
MONGO_INITDB_ROOT_PASSWORD=rootpassword
MONGO_INITDB_ROOT_USERNAME=root
MONGO_INITDB_DATABASE=cpa_data_dev
```

`DB_PW` and `DB_USER` should match `MONGO_INITDB_ROOT_PASSWORD` and `MONGO_INITDB_ROOT_USERNAME`

2.) Whipe DB

first take down containers `make down`

Remove docker volumes

```shell
docker volume prune

WARNING! This will remove all local volumes not used by at least one container.
Are you sure you want to continue? [y/N]
```

once this completes, bring images back up

`make up`

now api should return empty.

```shell
-> % curl -i -H "Accept: application/json" -H "Content-Type: application/json" http://localhost:8000/api/v1/subscriptions/
HTTP/1.1 200 OK
Date: Tue, 14 Apr 2020 17:25:34 GMT
Server: WSGIServer/0.2 CPython/3.8.2
Content-Type: application/json
Allow: GET, POST, HEAD, OPTIONS
X-Frame-Options: DENY
Content-Length: 2859
X-Content-Type-Options: nosniff

[]
```

Notes: see
[additional docker refs](https://linuxize.com/post/how-to-remove-docker-images-containers-volumes-and-networks/)
for trouble shooting Docker
