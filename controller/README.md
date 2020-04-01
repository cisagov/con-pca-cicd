# CPA Controller

## Setup:

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


### To access the Celery Flower dashboard:

- visit:
  - `localhost:5555/dashboard`