
APP_NAME=pfbex

DOCKER_REPO=motlib

pylint:
	pipenv run pylint --rcfile pylintrc fbexp


Pipfile.lock: Pipfile
	pipenv lock

requirements.txt: Pipfile.lock
	pipenv lock -r > $@

.PHONY: docker
docker:
	docker build -t $(APP_NAME) .;

docker_run: docker
	docker run --rm --env-file user.env -p 8765:8765 $(APP_NAME):latest

.PHONY: docker_publish
docker_publish: docker
	TAG=$$(git tag --points-at HEAD); \
	if [ ! -z "$${TAG}" ]; \
	then \
	  echo "Tagging docker image with '$${TAG}'."; \
	  docker tag $(APP_NAME) $(DOCKER_REPO)/$(APP_NAME):$${TAG}; \
	  docker push $(DOCKER_REPO)/$(APP_NAME):$${TAG}; \
	  \
	  docker tag $(APP_NAME) $(DOCKER_REPO)/$(APP_NAME):latest; \
	  docker push $(DOCKER_REPO)/$(APP_NAME):latest; \
	else \
	  echo "Tagging docker image with development tag."; \
	  docker tag $(APP_NAME) $(DOCKER_REPO)/$(APP_NAME):dev; \
	  docker push $(DOCKER_REPO)/$(APP_NAME):dev; \
	fi
