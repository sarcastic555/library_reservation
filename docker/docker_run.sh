#!/bin/zsh

docker run \
       -v ${LIBRARY_RESERVATION}:/home \
       -e TZ=Asia/Tokyo \
       -it \
       --rm \
       library_reservation
