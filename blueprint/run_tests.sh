#!/bin/sh

BASE_URL=${1:-${BASE_URL}}

pytest --tracing retain-on-failure --base-url $1
