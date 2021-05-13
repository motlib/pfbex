# This makefile automates building of the docker image (make docker), running a
# docker container for development (make docker_run) and deploying the container
# image to docker hub (make deploy).

# Application name
APP_NAME=pfbex

# Docker Hub repository name
DOCKER_USER=motlib
DOCKER_REPO=pfbex

# Architecture and version is determined automatically
ARCH := $(shell uname -m)
VERSION := $(shell git describe --always)

# Image tag names, both version specific and 'latest'
TAG_V=$(DOCKER_USER)/$(DOCKER_REPO):$(ARCH)-$(VERSION)
TAG_L=$(DOCKER_USER)/$(DOCKER_REPO):$(ARCH)-latest

# Color definitions for colored log output
C_INFO := $(shell tput setaf 2)
C_ERROR := $(shell tput setaf 1)
C_OFF := $(shell tput sgr0)

# Metadata file to update with the current version. See _update_version and
# _reset_version targets for details.
METADATA_FILE=pfbex/metadata.py


DOCKER_OPTS ?=
#--quiet


# Run linting
linting:
	@echo "$(C_INFO)Running pylint$(C_OFF)"

	./run.sh \
	  pylint \
	  --rcfile pylintrc \
	  pfbex

# Run unit tests
unittest:
	@echo "$(C_INFO)Running unit tests$(C_OFF)"
	./run.sh \
	  pytest \
	  pfbex


# Build docker development image
.PHONY: docker_dev
docker_dev:
	@echo "$(C_INFO)Building development docker image...$(C_OFF)"

	$(MAKE) \
	  TAG=$(APP_NAME):dev \
	  PIPENV_OPTS=--dev \
	  _docker


# Build runtime docker image
.PHONY: docker
docker:
	@echo "$(C_INFO)Building production docker image...$(C_OFF)"

	$(MAKE) \
	  TAG=$(APP_NAME) \
	  PIPENV_OPTS= \
	  _docker


# Build a docker image. TAG and DOCKER_OPTS variables have to be passed in.
.PHONY: _docker
_docker:
	$(MAKE) _update_version

	pipenv lock \
	  --keep-outdated \
	  --requirements \
	  $(PIPENV_OPTS) \
	> requirements.txt

	docker build \
	  --tag $(TAG) \
	  $(DOCKER_OPTS) \
	  .

	$(MAKE) _reset_version
	rm -f requirements.txt


# Build and run docker container (runtime environment)
docker_run: docker
	docker run \
	  --rm \
	  --env-file user.env \
	  -p 8765:8765 \
	  $(APP_NAME)


# Update metadata file with version identifier from git
.PHONY: _update_version
_update_version:
	@echo "$(C_INFO)Setting version in metadata file to '$(VERSION)'.$(C_OFF)"
	sed -i -E "s/^(APP_VERSION ).*/\\1= '${VERSION}'/g" $(METADATA_FILE)


# Reset the information in the metadata file, so we do not accidentally commit
# it.
.PHONY: _reset_version
_reset_version:
	@echo "$(C_INFO)Reset version info in metadata file$(C_OFF)"
	git checkout $(METADATA_FILE)


# Publish docker container to docker hub
.PHONY: deploy
deploy:
	@echo "$(C_INFO)Starting deployment process$(C_OFF)"

# We want to be sure to have nice and clean code before deploying.
	$(MAKE) linting
	$(MAKE) unittest

	$(MAKE) docker

# Check if we have built a release version (version is in X.Y.Z format). If not,
# we do not deploy.
	echo "$(VERSION)" | grep -Pq '^\d+\.\d+(\.\d+)?$$' \
	|| ( \
	  echo "$(C_ERROR)Not on a release version tag, so not publishing.$(C_OFF)"; \
	  exit 1;\
	)

	for tag in $(TAG_L) $(TAG_V); \
	do \
	  echo "$(C_INFO)Tagging docker image with '$${tag}' and pushing ...$(C_OFF)"; \
	  docker tag $(APP_NAME) $${tag}; \
	  docker push $${tag}; \
	done
