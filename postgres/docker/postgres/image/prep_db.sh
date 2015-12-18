#!/bin/bash

rm -rf /var/lib/pgsql/9.3/data
su --login - postgres --command "/usr/pgsql-9.3/bin/initdb -D /var/lib/pgsql/9.3/data -U postgres" || exit 1
mv /postgresql.conf /var/lib/pgsql/9.3/data
chown -v postgres.postgres /var/lib/pgsql/9.3/data/postgresql.conf

echo "host    all             all             0.0.0.0/0               md5" >> /var/lib/pgsql/9.3/data/pg_hba.conf

usermod -G wheel postgres || exit 1

su --login - postgres --command "/usr/pgsql-9.3/bin/postgres -D /var/lib/pgsql/9.3/data -p 5432" &
sleep 1
su --login - postgres --command "/usr/pgsql-9.3/bin/psql -c \"CREATE ROLE marsro;\"" || exit 1

PW=S3cr37
CMD="/usr/pgsql-9.3/bin/psql -c \"CREATE USER mobile with CREATEROLE superuser PASSWORD '$PW';\""
echo $CMD
su --login - postgres --command "$CMD" || exit 1

su --login - postgres --command "/usr/pgsql-9.3/bin/createdb -O mobile mobiledb-dev" || exit 1
su --login - postgres --command "/usr/pgsql-9.3/bin/psql -c \"\du;\"" || exit 1

su --login - mobile --command "/usr/pgsql-9.3/bin/psql mobiledb-dev < /schema.sql" || exit 1

su --login - postgres --command "/usr/pgsql-9.3/bin/pg_ctl -D /var/lib/pgsql/9.3/data stop"
