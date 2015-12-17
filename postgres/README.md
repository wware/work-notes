Postgres testing
================

At my job we use Postgres. Here I am tinkering with some ideas for dev-testing.

One thing that would be great would be a diff tool for schema versions. I favor keeping
the schema under version control, and generating delta scripts on an as-needed basis. I
don't mind throwing these scripts into version control as a historical record but I want
to think of them as derived, not fundamental.

Diffing schemas
---------------

Obviously you're going to want a diff tool for schemas. You could just take the output
of `"pg_dump --schema-only"` and try the standard UNIX `diff`, except that two schemas can
be exactly equivalent and still have a very complex diff. Tables and rows and functions etc.
may appear in a different order. SQL keywords may be uppercase or lowercase.
There may be comments that you don't care about diffing. There are
[other](http://www.liquibase.org/2007/06/the-problem-with-database-diffs.html)
[considerations](https://docs.google.com/presentation/d/1TV0bExFwVy-_d6C7A8Z2JL9Z9tvtkuZv3D58fkC3GWQ/edit)
that make schema diffing complex and interesting.

You can google `"postgres schema compare tool"` and see what has already been done.
One good candidate is [APGdiff](http://apgdiff.com/) ([Github](https://github.com/fordfrog/apgdiff)).
The Postgres community wiki has a
[big list of tools](https://wiki.postgresql.org/wiki/Community_Guide_to_PostgreSQL_GUI_Tools),
some relevant.

If I ran the Zoo
----------------

But it's fun to think a little bit about how I would do it. I'd first write a tool that
transformed a schema in a way that preserved functionality but made uniform all these
possible irrelevant differences. You might build this with
[psycopg2](http://initd.org/psycopg/) or [SQLAlchemy](http://www.sqlalchemy.org/), or it
might be smarter to use a Postgres grammar, either
[ANTLR](https://github.com/tunnelvisionlabs/antlr4-grammar-postgresql) for Java, or
[lex](https://github.com/postgres/postgres/blob/master/src/backend/parser/scan.l) and
[yacc](https://github.com/postgres/postgres/blob/master/src/backend/parser/gram.y).

* Indentation would be made uniform.
* There would be sections for tables, views, functions, triggers, etc. Sections would
  appear in a fixed order.
* Within each section, the objects would appear in alphabetical order by name.
* Within a table or view, columns would appear in alphabetical order by name.
* Keywords would appear in uppercase.

Dev testing
===========

Let's assume we find a viable diff tool and put schemas under version control. We can
meaningfully diff schemas, and (hopefully automatically) translate those diffs into delta
scripts. Next we need a process for testing database changes, and it needs to fit into the
process of doing releases to the production database. Confidentiality dictates that
production data must not be used in tests.

Grab a schema from post-release production after all hot fixes are done. This is the schema
you'll be updating at the next release night. In either local Docker or in AWS, spin up a
database instance. Write a script to drop the current database and create a database with the
production schema.

You'll to generate typical database content so that tests are realistic. Having initialized
an empty database with this randomly generated test data, you'll want to
[create a savepoint](http://www.postgresql.org/docs/8.3/static/tutorial-transactions.html).

Write tests using SQLAlchemy or psycopg2, and pytest or unittest. Each test starts by rolling
back to the savepoint. The savepoint should be right after the typical content has been
INSERTed. Tests must be as comprehensive as humanly possible.
