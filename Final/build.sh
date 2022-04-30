#!/bin/bash

tag=$1
if [ -z "$1" ]; then
    echo "No tag is provided, NOT going to push to docker hub."
    tag="TEST"
fi


cp ../../APIFramework.py ./APIFramework.py

docker build -t wenjin/final:$tag -t wenjin/final:latest ./

if [ "$tag" != "TEST" ]; then
    docker push wenjin/final:$tag
    docker push wenjin/final:latest
fi


rm -rf pygly pygly-scripts
rm APIFramework.py



