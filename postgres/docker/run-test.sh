#!/bin/sh

docker run -dP --name pg mars/postgres
py.test tryit.py 
docker rm -f pg
