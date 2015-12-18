#!/bin/bash

su --login - postgres --command "/usr/pgsql-9.3/bin/postgres -D /var/lib/pgsql/9.3/data -p 5432"
