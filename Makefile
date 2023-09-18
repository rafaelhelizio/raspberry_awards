include ./.env

PIP = ./venv/bin/pip

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


.PHONY: run test install venv

venv:
	python3 -m venv venv

## Install Application
setup: venv
	venv/bin/pip install -r requirements.txt

## Run Application and Install Application
setup-run: setup
	venv/bin/uvicorn main:app --host 0.0.0.0 --port 9000

## Run Application
run: 
	venv/bin/uvicorn main:app --host 0.0.0.0 --port 9000

## Run tests
test:
	 venv/bin/pytest


## Clean temp files
clean:
	rm -rf __pycache__ && rm -rf .pytest_cache && rm -rf venv && rm -rf raspberry_awards.log