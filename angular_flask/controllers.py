import os
import re # Regular Expressions
from flask import request, render_template, jsonify, session
from flask import send_from_directory, make_response
from flask.ext.socketio import emit, join_room, leave_room
from angular_flask import app, socketio

# routing for API endpoints, generated from the models designated as API_MODELS
from angular_flask.core import api_manager
from angular_flask.models import *

#Add logger to print to console
import logging
logger = logging.basicConfig()


# models for which we want to create API endpoints
for model_name in app.config['API_MODELS']:
    model_class = app.config['API_MODELS'][model_name]
    api_manager.create_api(model_class, methods=['GET', 'POST', 'PUT', 'PATCH'])

#Db session for making
db_session = api_manager.session

@socketio.on('join', namespace='/client')
def on_join(data):
    if data["queue"]:
        queue = data['queue']
        join_room(queue)

@socketio.on('leave', namespace='/client')
def on_leave(data):
    if data["queue"]:
        queue = data['queue']
        leave_room(queue)

@socketio.on('vote', namespace='/client')
def handle_voting(data):
    if data["vote_for"]:
        song = Song.query.filter(Song.id == int(data['vote_for'])).first()
        if song :
            song.votes = song.votes + 1
            db_session.commit()
            emit('vote', {'updated': [{'id': song.id, 'votes': song.votes}]}, room=song.queue_id)
        else:
            #TODO: Add Error Handling
            print("song doesnt exist")
	

@socketio.on('player-control', namespace='/client')
def handle_player_change(data):
    if "new" in data:
        songs = Song.query.filter(Song.queue_id == int(data["queue"])).order_by(Song.votes).all()
        print(songs)
        dictionary = dict()
        for song in songs:
            dictionary[song.votes] = song
        maxVotes = 0
        for votes in dictionary:
            if votes > maxVotes:
                maxVotes = votes
        emit('player-change', {'action': 'new','url': song.url}, room=song.queue_id)
        print(song, song.title, song.votes, song.queue_id)
        song.votes = 0
        db_session.commit()
        emit('vote', {'updated': [{'id': song.id, 'votes': song.votes}]}, room=song.queue_id)
        return
    elif "stop" in data:
        emit('player-change', {'action': 'stop'}, room=data['queue'])
        return
    elif "start" in data:
        emit('player-change', {'action': 'start'}, room=data['queue'])
        return
    elif "seek" in data:
        return

# routing for basic pages (pass routing onto the Angular app)
@app.route('/')
def index():
    return make_response(open('angular_flask/templates/index.html').read())

# routing for CRUD-style endpoints
# passes routing onto the angular frontend if the requested resource exists
from sqlalchemy.sql import exists

crud_url_models = app.config['CRUD_URL_MODELS']

#Routes for user creation and authentication
@app.route('/api/register', methods=['POST'])
def register():
    try:
    	json_data = request.json
	if json_data['username'] and json_data['password']:
		status = 'failure'
	
		# Sanitize username/password
		username = json_data['username']
		password = json_data['password']
		if isSafe(password):
			user = User(username=json_data['username'],
        	            password=json_data['password'].encode('utf-8'))
		        #TODO: Better error handling
		        #Check to see if the username already exists
		        if not User.query.filter(User.username==user.username).first():
		        	db_session.add(user)
		        	status = 'success'
		        	db_session.commit()
		        else:
		        	status = 'failure'
		else:
			status = 'unsafe'
	else:
        	status = 'failure'
    except:
	status = failure

    return jsonify({'result': status})

def isSafe(str):
	# For now, maxLen=100. 
	# Will need to check if we can allow arbitrarily long passwords
	upperCase = sum(1 for c in str if c.isupper())
	lowerCase = sum(1 for c in str if c.islower())
	digits = sum(1 for c in str if c.isnumeric())
	if len(str) > 10 and len(str) < 100 and upperCase > 0 and lowerCase > 0 and digits > 0:
		return True

	return False

@app.route('/api/login', methods=['POST'])
def login():
    json_data = request.json
    status = False
    #TODO: Better error handling and messages
    user = User.query.filter(User.username==json_data['username']).first()
    if user and bcrypt.check_password_hash(
            user.password, json_data['password']):
        user.active = True
        status = True
        db_session.commit()
    else:
        status = False
    return jsonify({'result': status})

@app.route('/api/logout', methods=['POST'])
def logout():
    json_data = request.json
    if json_data and json_data['username']:
        user = User.query.filter(User.username==json_data['username']).first()
        if user:
            user.active = False
            db_session.commit()
            return jsonify({'result': 'success'})
        else:
            return jsonify({'result': 'failure'})
    else:
        return jsonify({'result': 'failure'})


# special file handlers and error handlers
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/favicon.ico')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


