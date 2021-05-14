#!/bin/bash
#
# This file can be used to dump available service information from a FritzBox.
#
# Usage:
# 1) Edit user.env and specity at least username and password to log into the FritzBox
# 2) Run `./dump.sh`
# 3) You can find a `dump_xxxxxxx.csv` file in the directory where dump.csv is stored.
#

# The container image to use
CONTAINER_IMAGE=pfbex:latest

SRC_DIR=$(realpath $(dirname $0))

docker \
    run \
    --rm \
    -e DUMP_SERVICES=1 \
    -e DUMP_DATA=1 \
    --env-file user.env \
    --volume ${SRC_DIR}:/home/pfbex/app/output \
    --user $(id -u) \
    pfbex:latest
