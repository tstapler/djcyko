import os
import json
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template

from flask import Flask, request, Response
from flask import render_template, url_for, redirect, send_from_directory
from flask import send_file, make_response, abort

from flask import request, render_template
from flask import request, Response
from flask import render_template, url_for, send_from_directory
from flask import make_response, abort
from flask.ext.security import Security, login_required, SQLAlchemyUserDatastore
from angular_flask import app

# routing for API endpoints, generated from the models designated as API_MODELS
from angular_flask.core import api_manager
from angular_flask.models import *

# models for which we want to create API endpoints
app.config['API_MODELS'] = {'post': Post, 'song': Song, 'user': User, 'queue': Queue}

# models for which we want to create CRUD-style URL endpoints,

# and pass the routing onto our AngularJS application
app.config['CRUD_URL_MODELS'] = {'post': Post, 'song': Song, 'user': User, 'queue': Queue}
for model_name in app.config['API_MODELS']:
    model_class = app.config['API_MODELS'][model_name]
    api_manager.create_api(model_class, methods=['GET', 'POST', 'PUT', 'PATCH'])

session = api_manager.session

def handle_websocket(ws, url="" ):
	index = 0
	while True:
		message = ws.receive()
		if message is None:
			break
		else:
			message = json.loads(message)

	songs = session.query(Song).all()
	print len(songs)

#Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.route('/client', methods=['GET', 'POST'])
def client():
    return render_template('client.html')

# routing for basic pages (pass routing onto the Angular app)
@app.route('/')
@app.route('/about')
@app.route('/blog')
@app.route('/songs')
def basic_pages(**kwargs):
    return make_response(open('angular_flask/templates/index.html').read())

# routing for CRUD-style endpoints
# passes routing onto the angular frontend if the requested resource exists
from sqlalchemy.sql import exists

crud_url_models = app.config['CRUD_URL_MODELS']


@app.route('/<model_name>/')
@app.route('/<model_name>/<item_id>')
@app.route('/<model_name>/<item_id>/dj')
@app.route('/<model_name>/<item_id>/client')
def rest_pages(model_name, item_id=None):
    if model_name in crud_url_models:
        model_class = crud_url_models[model_name]
        if item_id is None or session.query(exists().where(
                model_class.id == item_id)).scalar():
            return make_response(open(
                'angular_flask/templates/index.html').read())
    abort(404)


# special file handlers and error handlers
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/favicon.ico')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


