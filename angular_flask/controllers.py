import os
import json

from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template, jsonify, session

from flask import request, Response
from flask import url_for, redirect, send_from_directory
from flask import send_file, make_response, abort

from flask import url_for, send_from_directory
from flask import make_response
from flask.ext.bcrypt import Bcrypt
from angular_flask import app

# routing for API endpoints, generated from the models designated as API_MODELS
from angular_flask.core import api_manager
from angular_flask.models import *

#Create hashing functionality
bcrypt = Bcrypt(app)

# models for which we want to create API endpoints
for model_name in app.config['API_MODELS']:
    model_class = app.config['API_MODELS'][model_name]
    api_manager.create_api(model_class, methods=['GET', 'POST', 'PUT', 'PATCH'])

db_session = api_manager.session

def handle_websocket(ws, url="xjB7J9dOtSM", queueID = 1):
	index = 0
	while True:
		f = open('ws.log', 'w')
		message = ws.receive()
		if message is None:
			break
		else:
			message = json.loads(message)

		songs = session.query(Song).all()
		dictionary = dict()
		for song in songs:
			dictionary[song.votes] = song

		maxVotes = 0
		for votes in dictionary:
			if votes > maxVotes:
				maxVotes = votes
		url = dictionary[maxVotes].url.partition('v=')[2][:11]
		f.write(url)
		f.write('\n')
		ws.send(json.dumps({'output':url}))

		toDelete = dictionary[maxVotes]
		toDelete.votes = 0

		session.add(toDelete)
		session.flush()

		f.close()

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
@app.route('/<model_name>/<item_id>/dj')
@app.route('/<model_name>/<item_id>/client')
def rest_pages(model_name, item_id=None):
    db_session = api_manager.session
    if model_name in crud_url_models:
        model_class = crud_url_models[model_name]
        if item_id is None or db_session.query(exists().where(
                model_class.id == item_id)).scalar():
            return make_response(open(
                'angular_flask/templates/index.html').read())
    abort(404)

#Routes for user creation and authentication
@app.route('/api/register', methods=['POST'])
def register():
    json_data = request.json
    user = User(username=json_data['username'],
                password=bcrypt.generate_password_hash(json_data['password'].encode('utf-8')))
    #Check to see if the username already exists
    if not db_session.query(User).filter(User.username==user.username).first():
        db_session.add(user)
        status = 'success'
        db_session.commit()
    else:
        status = 'this user is already registered'
    return jsonify({'result': status})

@app.route('/api/login', methods=['POST'])
def login():
    json_data = request.json
    status = False
    print(json_data['username'])
    try:
        user = User.query.filter_by(username=json_data['username']).first()
        if user and bcrypt.check_password_hash(
                user.password, json_data['password']):
            session['logged_in'] = True
            user.active = True
            status = True
            db_session.commit()
        else:
            status = False
    except:
        status = False
    return jsonify({'result': status})

@app.route('/api/logout', methods=['POST'])
def logout():
    json_data = request.json
    user = User.query.filter_by(username=json_data['username']).first()
    user.active = False
    db_session.commit()
    session.pop('logged_in', None)
    return jsonify({'result': 'success'})

# special file handlers and error handlers
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/favicon.ico')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


