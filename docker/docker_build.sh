#!/bin/zsh

docker build -t library_reservation . \
       --build-arg BOOKLOG_ID=${BOOKLOG_ID} \
       --build-arg BOOKLOG_PASSWORD=${BOOKLOG_PASSWORD}
