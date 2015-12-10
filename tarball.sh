#!/bin/sh

DEST=/media/sf_Shared/work-notes.tgz
(cd ..; tar cfz ${DEST} --exclude=venv work-notes/)
