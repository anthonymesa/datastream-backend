SHELL := /bin/bash

.PHONY: clean init run_dev dockerimage up down

DOCKERHUB = tcgdigitalus
IMAGE = image-name
VERSION = version
CONTAINER_NAME = tcgdigital-$(IMAGE)-$(VERSION)

PYTHON_COMMAND = $(shell python ./scripts/get_py.py)

ifeq ($(PYTHON_COMMAND),null)
	$(error Python 3 not found. Please install Python 3 and try again.)
endif

clean:
	@$(PYTHON_COMMAND) ./scripts/clean.py
	@echo Cleaned project.

init: clean
	@echo Initializing virtual environment...
	@$(PYTHON_COMMAND) ./scripts/init_venv.py
	@echo Initialization complete.

run_dev: init
	@$(PYTHON_COMMAND) ./scripts/run_dev.py

dockerimage:
	@echo Building docker image...
	@docker buildx build -t $(DOCKERHUB)/$(IMAGE):$(VERSION) --file Dockerfile .
	@echo Docker image build complete.

up: dockerimage
	@docker rm -f $(CONTAINER_NAME) && docker run -d --name $(CONTAINER_NAME) -p 8081:8081 --restart always $(DOCKERHUB)/$(IMAGE):$(VERSION)

down:
	@docker stop $(CONTAINER_NAME)
