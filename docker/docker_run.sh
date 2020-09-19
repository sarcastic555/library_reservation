#!/bin/zsh

docker run \
       -v ${PWD}/../:/home/ \
       -e TZ=Asia/Tokyo \
       -it \
       --rm \
       library_reservation
