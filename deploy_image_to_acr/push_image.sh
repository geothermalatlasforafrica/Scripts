#!/bin/bash

# This script build the docker image from the dockerfile specified in the command and pushes it
# to the Azure Container Registry (ACR). "myacicontext" refers to the ACR.

docker --version
if [ $? -eq 0 ]; then
    echo OK - DOCKER IS RUNNING
else
    echo FAIL - DOCKER IS NOT RUNNING
    exit 1
fi

NAME=$1
VERSION=$2
REGISTRY=$3
DOCKERFILE_PATH=$4
CONTEXT_PATH=$5

az account set --subscription "d8d3dd94-5be7-4359-9a29-d31257033626"

docker context use myacicontext

az acr build --image ${NAME}:${VERSION} --registry ${REGISTRY} --file ${DOCKERFILE_PATH} ${CONTEXT_PATH}

docker context use default

echo FINISHED PUBLISHING ${NAME}:${VERSION}