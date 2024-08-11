#!/bin/bash

REGISTRY_URL=192.168.178.100:10001
IMAGE_NAME=youtube_analyzer

# Exit if no Docker image version was passed as argument
if [[ -z "$1" ]]; then
    echo "Please pass the new Docker image version as argument!"
    exit 1

# Build and push the test image without any checks and questions
elif [[ "$1" == "test" ]];  then
    docker build -t $REGISTRY_URL/$IMAGE_NAME:$1 .
    docker push $REGISTRY_URL/$IMAGE_NAME:$1

# Befor building and pushich check if the image tag already exist.
else
    # Check if `skopeo` is installed
    if command -v skopeo &> /dev/null; then
        # Check if the version tag is already in the remote registry and ask for confirmation to override
        if [[ $(skopeo inspect --tls-verify=false docker://$REGISTRY_URL/$IMAGE_NAME | jq -r '.RepoTags[]') =~ $1 ]]; then
            read -n 1 -s -r -p "Version tag already exist in remote registry. Override? [y|N] " continue; echo

            if [[ "$continue" != "y" ]]; then
                exit 1
            fi
        fi
    # Check if the version tag is already locally available and ask for confirmation to override
    elif [[ -n "$(docker images -q $REGISTRY_URL/$IMAGE_NAME:$1)" ]]; then
        read -n 1 -s -r -p "Version tag already exist locally. Override? [y|N] " continue; echo

        if [[ "$continue" != "y" ]]; then
            exit 1
        fi
    fi

    # Build and push the Docker image to the remote registry
    docker build -t $REGISTRY_URL/$IMAGE_NAME:latest -t $REGISTRY_URL/$IMAGE_NAME:$1 .
    docker push $REGISTRY_URL/$IMAGE_NAME:$1
    docker push $REGISTRY_URL/$IMAGE_NAME:latest
fi
