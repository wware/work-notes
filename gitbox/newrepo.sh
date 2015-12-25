#!/bin/sh

REPO=$(basename $1)

(cd $1/.git; tar cf - .) | \
ssh gitbox "(mkdir -p /opt/git/$REPO.git; cd /opt/git/$REPO.git; tar xf -)"
