from datetime import datetime

from angular_flask.core import db
from flask.ext.security import UserMixin
from flask.ext.bcrypt import Bcrypt
from angular_flask import app

#Create hashing functionality
bcrypt = Bcrypt()

class Queue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=True)
    songs = db.relationship('Song', backref='queue', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, user_id):
        self.title = title
        self.user_id = user_id

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
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

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    queues = db.relationship('Queue', backref='user', lazy='dynamic')

    def __init__(self, username, password, active=False):
        self.username = username
        self.password = bcrypt.generate_password_hash(password)
        self.acive = active

    def __repr__(self):
        return self.username

# models for which we want to create API endpoints
app.config['API_MODELS'] = {'song': Song, 'user': User, 'queue': Queue}

# models for which we want to create CRUD-style URL endpoints,
# and pass the routing onto our AngularJS application
app.config['CRUD_URL_MODELS'] = { 'song': Song, 'user': User, 'queue': Queue}
