import os
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template
from angular_flask import app,my_app

def runserver():
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    http_server = WSGIServer(('',5000), my_app, handler_class=WebSocketHandler)
    http_server.serve_forever()
    runserver()
