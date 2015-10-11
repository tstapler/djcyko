import os
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from werkzeug.serving import run_with_reloader
from flask import Flask, request, render_template
from angular_flask import app,my_app

@run_with_reloader
def runserver():
    http_server = WSGIServer(('',5000), my_app, handler_class=WebSocketHandler)
    http_server.serve_forever()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    runserver()
