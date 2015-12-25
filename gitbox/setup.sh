#!/bin/sh

sudo mkdir -p /opt/git || exit 1
sudo chown -R wware:wware /opt/git || exit 1

if [ ! -d /opt/git/.git ]
then
    cp -r foo.git /opt/git/.git || exit 1
fi

if [ -z "$(docker images | grep gitbox)" ]
then
    docker build -t gitbox . || exit 1
fi
docker run -dP -p 80:1234 --name=gitbox -v /opt/git:/opt/git gitbox
