#!/bin/bash

#### for simple debug
# D=echo
D=""

function build() {
  ${D} docker build -t pyapi:1 .
} 

function rmapi() {
  ${D} docker rm api
}

function rerun () {
  rmapi
  runapi
}

function runapi () {
  ${D} docker run --name api -p 5000:5000 pyapi:1
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

