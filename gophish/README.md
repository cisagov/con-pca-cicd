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
- Restart proxy to reflect changes
  - `docker exec -it pca-gophish-proxy service nginx restart`
- GoPhish admin UI is running on `localhost` & `localhost:3333`
- Phishing server is running on `localhost:8080`
- Adminer UI is running on `localhost:9000`

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

## Setup on a Production Server

### Initial Setup

- Clone this repo
- Create your env file in to the root directory
  - `cp etc/env.dist .env`
- Change the `server_name` in `etc/nginx/config.conf` from `127.0.0.1`
to [your domain name]
- Update your `.env` file to a more secure database password
- Install **Make**
  - `sudo apt install make`

### Run GoPhish on a Production Server

- Install and update required packages
  - `make init`
- Follow on-screen prompts
- Restart Server in order for changes to take effect
- Build containers
  - `cd gophish-prod`
  - `make build`
- Run GoPhish
  - `make up`

#### Generate SSL Certificates using Let's Encrypt

- Shell into the Nginx container:
  - `docker exec -it pca-gophish-proxybash`
- Run Certbot:
  - `certbot --nginx`
- Follow on-screen prompts
- Restart Nginx service
  - `service nginx restart`
  - **Note:** the shell will close because this command restarts the container
- Restart the Nginx container
  - `make up`
- Visit your domain to access the GoPhish admin UI
