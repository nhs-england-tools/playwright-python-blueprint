#!/bin/sh

BASE_URL=${1:-${BASE_URL}}
TAG_TO_USE=${2:=${TAG_TO_USE}}
export COGNITO_USER_PASSWORD=${3:=${COGNITO_USER_PASSWORD}}

pytest --tracing retain-on-failure --base-url $1 -m $2
