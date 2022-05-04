#!/bin/bash

tag="V0.0.1"

docker build -t wenjin27/visfinal:$tag -t wenjin27/visfinal:latest ./

docker push wenjin27/visfinal:$tag
docker push wenjin27/visfinal:latest



