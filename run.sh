#!/bin/bash -eux

THIS_DIR=$(dirname $0)

source "${THIS_DIR}/credentials.sh"

exec python -u "${THIS_DIR}/server.py"
