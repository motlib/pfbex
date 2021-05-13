#!/bin/bash
#
# This file can be used to start a command inside the development docker
# container
#
# Usage: ./run.sh <COMMAND>
#

make -s DOCKER_OPTS=--quiet docker_dev

SRC_DIR=$(realpath $(dirname $0))

docker \
    run \
    -p 8765:8765 \
    --rm \
    --env-file user.env \
    --volume ${SRC_DIR}:/home/pfbex/app \
    -it \
    --user $(id -u) \
    pfbex:dev \
    $*
