import os
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from werkzeug.serving import run_with_reloader
from socketio.server import SocketIOServer
from angular_flask import app, socketio
from gevent import monkey

def runserver():
    monkey.patch_all()
    app.debug = True
    socketio.run(app)
    SocketIOServer(('',5000),app,resource="socket.io").serve_forever()

if __name__ == '__main__':
    runserver()
