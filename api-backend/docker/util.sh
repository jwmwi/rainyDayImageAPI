#!/bin/bash

IMAGE_NAME=rainydayimageapi
IMAGE_VERSION=1.0.0
IMAGE=${IMAGE_NAME}:${IMAGE_VERSION}
CONTAINER_NAME=api
IMAGE_DIRECTORY=~/images.cache

#### for simple debug
# D=echo
D=""

function build() {
  ${D} docker build -t ${IMAGE} .
} 

function rmapi() {
  ${D} docker rm ${CONTAINER_NAME}
}

function rerun () {
  rmapi
  runapi
}

function runapi () {
  ${D} docker run \
      -v ${IMAGE_DIRECTORY}:/images \
      --env-file .env \
      --name ${CONTAINER_NAME} \
      -p 5000:5000 \
      ${IMAGE}
}

function rebuild () {
  build
  rerun
}

case $1 in 
  "build" )
    build;
    ;;
  "rerun" )
    rerun;
    ;;
  "run" )
    runapi;
    ;;
  "rebuild" )
    rebuild;
    ;;
  "rm" )
    rmapi;
    ;;
  *)
    echo "ERROR: "
    echo "    USAGE: $0 [build|rerun|run|rebuild|rm]"
    echo
    echo "    build - build the container"
    echo "    rerun - rm container instance then run again "
    echo "    run -  run the container "
    echo "    rebuild - rebuild then run"
    echo "    rm - just rmove the conatiner"
    echo
    exit 1
    ;;
esac

