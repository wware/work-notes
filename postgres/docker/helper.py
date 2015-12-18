import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

DB_PW = 'S3cr37'
DB_IP_ADDR = os.popen(
    "docker inspect --format='{{.NetworkSettings.IPAddress}}' pg"
).read().strip()
assert DB_IP_ADDR, "Run: docker run -dP --name pg mars/postgres"

SQLALCHEMY_DATABASE_URI = (
    'postgresql://mobile:{0}@{1}/mobiledb-dev'.format(DB_PW, DB_IP_ADDR)
)
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)
