#!/bin/bash

BASE_URL=$1
MARKERS_TO_USE="${2//-/ }" # replace hyphens with spaces
export COGNITO_USER_PASSWORD=$3

pytest --tracing retain-on-failure --base-url $BASE_URL -m "$MARKERS_TO_USE"
