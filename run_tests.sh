#!/bin/sh

BASE_URL=${1:-${BASE_URL}}

pytest --base-url $1
