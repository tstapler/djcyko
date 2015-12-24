import os
import json
from flask import Flask, request, Response
from flask import render_template, send_from_directory, url_for
from flask.ext.socketio import SocketIO

app = Flask(__name__)
app.config.from_object(os.getenv('CONFIG','angular_flask.settings.Config'))
app.url_map.strict_slashes = False

#Initialize websocket handler
socketio = SocketIO(app)

import angular_flask.core
import angular_flask.models
import angular_flask.controllers
