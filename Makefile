include ./.env

# COLORS
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)


TARGET_MAX_CHAR_NUM=20


## Show help
help:
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)

# Build docker image
build:
	docker build -t fastapiexample --no-cache --build-arg GITLAB_PACKAGES=${GITLAB_PACKAGES} .


## Run main.py
no-container:
	python main.py

## Run API in docker image
run: rm
	docker run --env-file .env -p ${APPLICATION_PORT}:8000 --name fastapiexample fastapiexample

## Run API in docker image using backend network
run-local: rm
	docker run --env-file .env  --network ${DEV_CONTAINER_NETWORK} -p ${APPLICATION_PORT}:8000 --name fastapiexample fastapiexample

## Start API container
start:
	docker start fastapiexample

## Stop container
stop:
	docker stop fastapiexample

## Remove container
rm:
	-docker rm fastapiexample -f

## Remove image
rmi:
	docker rmi fastapiexample

## Container bash
exec:
	docker exec -it fastapiexample /bin/sh

## Run tests
test:
	docker exec fastapiexample pytest --cov=app/

## Start database
init-db:
	for script in ./db/init_db/*.sql; do cat "$script" | docker exec -i pg_container psql -U ${DATABASE_USER} -d ${DATABASE_NAME}; done

## Make migrations
migrate:
	docker run --rm -v $(dir $(realpath $(lastword $(MAKEFILE_LIST))))/db/migrations:/flyway/sql -e FLYWAY_EDITION=community --network backend flyway/flyway:9-alpine -url=jdbc:postgresql://${DATABASE_HOST}:5432/${DATABASE_NAME} -schemas=flyway -user=${DATABASE_USER} -password=${DATABASE_PASSWORD} -connectRetries=10 migrate
