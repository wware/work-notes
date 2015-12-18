Database testing with Docker
====

The idea here is to create a Docker instance that runs Postgres and is
loaded with a schema but no data. This is useful for testing database-related
stuff -- anything involving psychopg2 or SQLAlchemy will work with this
instance, as well as SQL changes.

This instance will not use persistent data. Every time it starts, it will
start with an empty database. You want to start tests from a known point so
that results are reproducible, and independent of the order in which tests run.
Docker instances do not save any changes to their contents unless you do so
intentionally (`docker commit`).

Getting started
----

Begin by installing Docker on your Linux VM. The docker.io package in the
standard Ubuntu repository is too old and busted and crappy.

```
$ curl -sSL https://get.docker.com/ | sh
$ sudo usermod -a -G docker <username>
```

Put this line in the file `/etc/default/docker`.

```
DOCKER_OPTS="--dns 8.8.8.8 --dns 8.8.4.4 --bip=192.168.0.1/24"
```

Then, as root, run these commands.

```
stop docker
ip link del docker0
start docker
```

To run the example test, simply:

```
./build.py postgres
./run-test.sh
```
