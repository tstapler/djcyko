from datetime import datetime

from angular_flask.core import db
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

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True)
    url = db.Column(db.String(200))
    votes = db.Column(db.Integer)
    playing = db.Column(db.Boolean)

    def __init__(self, title, url, votes, playing):
        self.title = title
        self.url = url
        self.votes = votes
        if(playing is None):
            self.playing = False
        else:
            self.playing = playing

    def __repr__(self):
        return '<Song %r>' % self.title

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

# models for which we want to create API endpoints
app.config['API_MODELS'] = {'post': Post, 'song': Song, 'user': User}

# models for which we want to create CRUD-style URL endpoints,
# and pass the routing onto our AngularJS application
app.config['CRUD_URL_MODELS'] = {'post': Post, 'song': Song, 'user': User}
