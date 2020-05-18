# Con-PCA

## Continuous Phishing Assessment

### Project Directory

- [Client](https://github.com/cisagov/con-pca/tree/develop/client)
- [Controller](https://github.com/cisagov/con-pca/tree/develop/controller)
- [GoPhish](https://github.com/cisagov/con-pca/tree/develop/gophish)

### Requirements

For local setup, Get the right flavor of Docker for your OS...

- [Docker for Mac](https://docs.docker.com/docker-for-mac/install/)
- [Docker for Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
- [Docker for Windows](https://docs.docker.com/docker-for-windows/install/)

**Note:** The recommended requirement for deployment of this project is 4 GB RAM.
For Docker for Mac, this can be set by following these steps:

Open Docker > Preferences > Advanced tab, then set memory to 4.0 GiB

## Local Install and Deployment

### Git Clone Project

Make sure you have a github account and access to the correct repo.

To install project run

```shell
git clone git@github.com:cisagov/con-pca.git
```

Use `Makefile` to install and run all services.

### Setup and Build

Create your .env files

- `make env`
- **note**: reach out to someone to update your `.env` files with project secrets

Build containers:

- `make build`

To run the containers, use:

- `make up`

Your output will look like:

```shell
-> % make up
Creating pca-rabbitmq ... done
Creating pca-mongodb  ... done
Creating pca-web      ... done
Creating pca-worker   ... done
Creating pca-beat     ... done
Creating pca-api      ... done
```

Stop containers

- `make stop`

Remove containers

- `make down`

## Project Components

For more information regarding each component,

- Please see [here](client/README.md) for the client service
- Please see [here](controller/README.md) for the controller service
- Please see [here](gophish/README.md) for the gophish service

## Dev Access

You can use these enpoints to debug and develop, suggested access:

- [curl](https://curl.haxx.se/docs/manpage.html)

- [PostMan](https://www.postman.com/)

## Api

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

## Contributing

We welcome contributions!  Please see [here](CONTRIBUTING.md) for
details.

## License

This project is in the worldwide [public domain](LICENSE).

This project is in the public domain within the United States, and
copyright and related rights in the work worldwide are waived through
the [CC0 1.0 Universal public domain
dedication](https://creativecommons.org/publicdomain/zero/1.0/).

All contributions to this project will be released under the CC0
dedication. By submitting a pull request, you are agreeing to comply
with this waiver of copyright interest.
