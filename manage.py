import os
import json
import requests

from sqlalchemy.sql import table, column
from sqlalchemy import *
from alembic import op
from alembic.operations import Operations
from alembic.migration import MigrationContext
from flask.ext.script import Manager, Command, Option
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.bcrypt import Bcrypt

from angular_flask.core import db, app

metadata = MetaData()
manager = Manager(app)

#Establish Alembic Operatoins object
engine = create_engine(os.getenv('DATABASE_URL'))
conn = engine.connect()
ctx = MigrationContext.configure(conn)
op = Operations(ctx)

bcrypt = Bcrypt()

@manager.command
def create_db():
    db.create_all()

@manager.command
def delete_db():
    db.session.close()
    db.drop_all()

@manager.option('-f', '--seedfile', help='File containing json to be added to the database')
def seed_db(seedfile):
    with open(seedfile, 'r') as f:
        seed_data = json.loads(f.read())
        for table_name in seed_data:
           if table_name == "user":
               for number, user in enumerate(seed_data[table_name]):
                   seed_data[table_name][number]["password"] = bcrypt.generate_password_hash(user["password"])
           table_to_insert = Table(table_name, metadata, autoload=True, autoload_with=engine) 
           op.bulk_insert(table_to_insert, seed_data[table_name])

        print "\nSample data added to database!"

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
