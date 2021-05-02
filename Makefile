# This makefile automates building of the docker image (make docker), running a
# docker container for development (make docker_run) and deploying the container
# image to docker hub (make deploy). 

# Application name
APP_NAME=pfbex

# Docker Hub repository name
DOCKER_REPO=motlib

# Architecture and version is determined automatically
ARCH := $(shell uname -m)
VERSION := $(shell git describe --always)

# Image tag names, both version specific and 'latest'
TAG_V=$(DOCKER_REPO)/$(APP_NAME)-$(ARCH):$(VERSION)
TAG_L=$(DOCKER_REPO)/$(APP_NAME)-$(ARCH):latest


# Color definitions for colored log output
INFO := $(shell tput setaf 2)
ERROR := $(shell tput setaf 1)
OFF := $(shell tput sgr0)

# Metadata file to update with the current version. See _update_version and
# _reset_version targets for details.
METADATA_FILE=pfbex/metadata.py


# Run linting
pylint:
	@echo "$(INFO)Running pylint$(OFF)"
	pipenv run pylint \
	  --rcfile pylintrc \
	  pfbex service_dumper.py


# Build docker image
.PHONY: docker
docker: 
	@echo "$(INFO)Building docker image...$(OFF)"

	$(MAKE) _update_version

	docker build \
	  --tag $(APP_NAME) .

	$(MAKE) _reset_version


# Build and run docker container
docker_run: docker
	docker run \
	  --rm \
	  --env-file user.env \
	  -p 8765:8765 \
	  $(APP_NAME)


# Update metadata file with version identifier from git
.PHONY: _update_version
_update_version:
	@echo "$(INFO)Setting version in metadata file to '$(VERSION)'.$(OFF)"
	sed -i -E "s/^(APP_VERSION ).*/\\1= '${VERSION}'/g" $(METADATA_FILE)


# Reset the information in the metadata file, so we do not accidentally commit
# it.
.PHONY: _reset_version
_reset_version:
	@echo "$(INFO)Reset version info in metadata file$(OFF)"
	git checkout $(METADATA_FILE)


# Publish docker container to docker hub
.PHONY: deploy
deploy: docker
	@echo "$(INFO)Starting deployment process$(OFF)"

# We want to be sure to have nice and clean code before deploying.
	$(MAKE) pylint

	$(MAKE) docker

# Check if we have built a release version (version is in X.Y.Z format). If not,
# we do not deploy.
	echo "$(VERSION)" | grep -Pq '^\d+\.\d+(\.\d+)?$$' \
	|| ( \
	  echo "$(ERROR)Not on a release version tag, so not publishing.$(OFF)"; \
	  exit 1;\
	)

	for tag in $(TAG_L) $(TAG_V); \
	do \
	  echo "$(INFO)Tagging docker image with '$${tag}' and pushing ...$(OFF)"; \
	  docker tag $(APP_NAME) $${tag}; \
	  docker push $${tag}; \
	done

