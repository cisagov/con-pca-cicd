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

### To access the Angular app:
  - visit:
    - `localhost:4200`

### To access the Django API:
  - visit:
    - `localhost:8000`

### To access the Celery Flower dashboard:
- visit:
  - `localhost:5555/dashboard`

### To access the RabbitMQ dashboard:
- visit:
  - `localhost:15672`
