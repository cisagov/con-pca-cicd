# Con-PCA GoPhish

## Features

- [Docker](https://www.docker.com/)
- [Nginx](https://www.nginx.com/)
- [Let's Encrypt](https://letsencrypt.org/)
- [MySQL Database](https://www.mysql.com/)
- [Adminer database management UI](https://www.adminer.org/)
- Tested to launch on an Ubuntu 18.04 LTS Server

## Requirements

For local setup, Get the right flavor of Docker for your OS...

- [Docker for Mac](https://docs.docker.com/docker-for-mac/install/)
- [Docker for Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
- [Docker for Windows](https://docs.docker.com/docker-for-windows/install/)

**Note:** The recommended requirement for deployment of this project is 4 GB RAM.
For Docker for Mac, this can be set by following these steps:

Open Docker > Preferences > Advanced tab, then set memory to 4.0 GiB

A registered domain name

## Setup locally

- Create your env file
  - `cp etc/env.dist .env`
- Build containers
  - `make build`
- Run GoPhish
  - `make up`
- Return GoPhish app logs
  - `make logs`

- GoPhish admin UI is running on `localhost` & `localhost:3333`
- Phishing server is running on `localhost:8080`

## Set up webhooks

- Log onto admin UI located at `localhost:3333`
- Naviagate to "Webhooks" panal
- select: `+ New Webhook`
  - name: `Local Webhook`
  - url: `http://pca-api:8000/api/v1/inboundwebhook/`
  - Is active: `true`
  - Save!
- test the connection via `ping` button
- Webhooks are now setup for `con-pca`

### GoPhish Credentials
- run `docker logs pca-gophish`
  - look for your username and password
- visit: `localhost:3333`
  - login with the credentials found in the logs
  - update your password

### Stop and Remove project containers

- Stop all containers
  - `make stop`
- Remove all containers
  - `make down`
