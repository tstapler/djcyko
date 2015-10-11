from datetime import datetime

from angular_flask.core import db
from flask.ext.security import UserMixin, RoleMixin
from angular_flask import app

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, body, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date

    def __repr__(self):
        return '<Post %r>' % self.title

class Queue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    songs = db.relationship('Song', backref='queue', lazy='dynamic')
    def __init__(self, title):
        self.title = title

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True)
    url = db.Column(db.String(200))
    votes = db.Column(db.Integer)
    playing = db.Column(db.Boolean)
    queue_id = db.Column(db.Integer, db.ForeignKey('queue.id'))

    def __init__(self, title, url, votes, playing, queue_id):
        self.title = title
        self.url = url
        self.votes = votes
        self.queue_id = queue_id
        if(playing is None):
            self.playing = False
        else:
            self.playing = playing

    def __repr__(self):
        return '<Song %r>' % self.title

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

# models for which we want to create API endpoints
app.config['API_MODELS'] = {'post': Post, 'song': Song, 'user': User, 'queue': Queue}

# models for which we want to create CRUD-style URL endpoints,
# and pass the routing onto our AngularJS application
app.config['CRUD_URL_MODELS'] = {'post': Post, 'song': Song, 'user': User, 'queue': Queue}
