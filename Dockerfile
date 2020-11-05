# Python support can be specified down to the minor or micro version
# (e.g. 3.6 or 3.6.3).
# OS Support also exists for jessie & stretch (slim and full).
# See https://hub.docker.com/r/library/python/ for all supported Python
# tags from Docker Hub.
FROM python:3.8-alpine

LABEL Name=fbexp Version=0.0.1
EXPOSE 8765

WORKDIR /app
ADD . /app

# Using pip:
#RUN apk add --no-cache libxml2 libxslt
#RUN apk add --no-cache --virtual .build-deps gcc musl-dev libxml2-dev libxslt-dev \
#        && python3 -m pip --no-cache-dir install -r requirements.txt \
#        && apk del .build-deps

RUN  python3 -m pip --no-cache-dir install -r requirements.txt


CMD ["python3", "-m", "fbexp"]
