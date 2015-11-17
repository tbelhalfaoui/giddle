import os
import psycopg2
import urlparse
from peewee import *
from playhouse.postgres_ext import *


url = urlparse.urlparse(os.environ["HEROKU_POSTGRESQL_GOLD_URL"])
urlparse.uses_netloc.append("postgres")
db = PostgresqlExtDatabase(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port,
        register_hstore=False)


class DBElement(Model):
    class Meta:
        database = db
    
    def __repr__(self):
        return str(self._data)

    def __str__(self):
        return repr(self)