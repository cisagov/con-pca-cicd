# Con-PCA Controller

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
git clone git@github.com:cisagov/con-pca.git
cd con-pca/controller
```

Use `Makefile` to install and run `controller` services.

### Setup and Build

To create `.env` files for containers, use this command to generate them.
These files are used as configuration in deployment.

Create your .env file

- `cp etc/env.dist .env`
- **Note:** visit `localhost:3333/settings` to get your API key. Save it into your `.env` file

Build containers

- `make build`

Run your web application locally

- `make up`

Run Django logs in the terminal

- `make logs`

Initialize GoPhish & generate random data into mongo
- `make init`

Stop containers

- `make stop`

Remove containers

- `make down`

Access Django shell

- `make shell`

Drop DB of all data

- `make db_drop_mongo`

### Creating and loading random data

Using the makefile command: `make db_load_dummy` you can create data in
the db and get an output file containing all the id's of the created data.

Incase you want to clear out all data in the DB, use: `make db_drop_mongo`

WARNING: This will drop ALL DATA in the connected docker mongodb

### Example

```shell
-> % make db_load_dummy
python scripts/create_dummy_data.py
loading dummy json data
done loading data
Step 1/3: create templates...
created tempaltes_list: [u'883e0f1f-2b7a-44e9-a49d-5d9d231fd943', u'0a4ab912-25de-4e9c-bcc7-fb9a88427e36']
Step 2/3: create targets...
created target_list: [u'9079a1ad-3ed0-4ee8-a181-57bec0005f5a', u'd504b75a-4331-47a0-bfd7-c2e7c03540fe', u'32f16b48-3eec-4fc9-8dd6-cd07333daa26', u'23cd3a99-192f-4874-999f-2d9aa18b45ed', u'3d625281-e0bf-4d13-a07d-9e83139fc412', u'ee4d6547-4701-4286-ac27-c690625c1c76', u'8f993439-3046-4217-bcea-c771c33cae7f']
Step 3/3: create subscriptions...
created subcription_list: [u'd25ae2c4-0f0a-4bf3-a86e-9c4f5950b2ca', u'aef12cdb-bb42-48d4-9a85-345a1f0e9967', u'763daf22-8f9d-4a0a-bc95-12538cd391a5', u'cd71d0ce-b61f-4763-a7d8-c7f01d411b05', u'a34869b0-ebf8-44bb-9b9e-ebd4f12a0b07', u'e494b918-052f-4e78-92a5-034d477b83d0', u'5d2b8b9e-12c9-4f3e-a76d-2a6bf54be5b0', u'1e79bfb1-6ef8-4671-9413-45015263d29f', u'c74cf69d-634d-4f77-a93a-d96c072ea2f9', u'95db5067-a9ac-4865-978d-c6753e39edb8', u'3f4f712a-25cf-4357-98ab-1a33037375fa', u'd83d7ad0-9feb-4471-8705-8af80580fe59', u'3af315cf-30c8-4123-ab37-bdd295325701']
writting values to file: /.../con-pca/controller/scripts/data/created_dummy_data_2020_04_15_155141.json...
Finished.....
```

As seen this will output data files into
`scripts/data/created_dummy_data_2020_04_15_155141.json.` location and
will genrate a new file every time it is ran. These files will not be
checked into github and will remain on a devs system.

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
Creating pca-rabbitmq ... done
Creating pca-mongodb  ... done
Creating pca-worker   ... done
Creating pca-beat     ... done
Creating pca-api      ... done
```

Dev Access

You can use these endpoints to debug and develop, suggested access:

- [drf-yasg - Yet another Swagger generator](https://drf-yasg.readthedocs.io/en/latest/)

- [curl](https://curl.haxx.se/docs/manpage.html)

- [PostMan](https://www.postman.com/)

### drf-yasg / Swagger

Here we are using genrated docs via swagger that also give us a
few ways of viewing them.

Once running, navigate to the
[Api Swagger UI](http://localhost:8000/api/v1/swagger/)
located at: `http://localhost:8000/api/v1/swagger/`

You can also see the redoc version of the api at, navigate to the
[Api redoc UI](http://localhost:8000/api/v1/redoc/)
located at: `http://localhost:8000/api/v1/redoc/`

To download the api docs as yaml or json, use the following enpoints:
[Api Swagger json](http://localhost:8000/api/v1/swagger.json)
[Api Swagger YAML](http://localhost:8000/api/v1/swagger.yaml)

Here you can see how the calls are defined. These objects are defined under `api.serializers.*`
When created, it is genrated from those files and is validated when sending.

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
MONGO_INITDB_DATABASE=pca_data_dev
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
