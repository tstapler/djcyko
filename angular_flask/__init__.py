import os
import json
from flask import Flask, request, Response
from flask import render_template, send_from_directory, url_for

app = Flask(__name__)
app.config.from_object('angular_flask.settings')
app.url_map.strict_slashes = False

import angular_flask.core
import angular_flask.models
import angular_flask.controllers

def my_app(environ, start_response):
    path = environ["PATH_INFO"]
    if path == "/":
        return app(environ, start_response)
    elif path == "/websocket":
        angular_flask.controllers.handle_websocket(environ["wsgi.websocket"])
        return DebuggedApplication(app)
    else:
        return app(environ, start_response)

