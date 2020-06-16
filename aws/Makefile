# target: logs - Runs all logs into the terminal
logs:
	docker-compose logs

# target: build - Builds containers
build:
	docker-compose build

# target: up - Starts localstack and provisions terraform resources. Will also reapply terraform.
up:
	docker-compose up -d

# target: stop - Stops all docker containers
stop:
	docker-compose stop

# target: down - Removes all docker containers
down:
	docker-compose down

# target: resest - Removes docker containers, rebuilds, removes volumes and restarts
reset:
	docker-compose down
	docker-compose build
	docker volume rm aws_pca-terraform-data
	docker volume rm aws_pca-localstack-data
	docker-compose up -d

# target: tflogs - outputs terraform logs
tflogs:
	docker logs pca-terraform
