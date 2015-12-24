import os
import json
import argparse
import requests

from flask.ext.script import Manager, Command, Option
from flask.ext.migrate import Migrate, MigrateCommand

from angular_flask.core import db, app
manager = Manager(app)

@manager.command
def create_sample_db_entry(api_endpoint, payload):
    url = 'http://localhost:' + os.getenv('PORT','5000') + '/' + api_endpoint
    r = requests.post(
            url, data=json.dumps(payload),
            headers={'Content-Type': 'application/json'})
    print r.text

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

    for item_class in seed_data:
        items = seed_data[item_class]
        print items
        for item in items:
            print item
            create_sample_db_entry('api/' + item_class, item)

    print "\nSample data added to database!"

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
