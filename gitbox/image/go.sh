#!/bin/sh

(cd /opt/git; git instaweb --httpd=webrick)
/usr/sbin/sshd -D
