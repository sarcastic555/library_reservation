#!/bin/zsh

docker build -t library_reservation . \
       --build-arg BOOKLOG_ID=${BOOKLOG_ID} \
       --build-arg BOOKLOG_PASSWORD=${BOOKLOG_PASSWORD} \
       --build-arg ICHIKAWA_LIBRARY_ID=${ICHIKAWA_LIBRARY_ID} \
       --build-arg ICHIKAWA_LIBRARY_PASSWORD=${ICHIKAWA_LIBRARY_PASSWORD} \
       --build-arg CULIL_API_KEY=${CULIL_API_KEY}
