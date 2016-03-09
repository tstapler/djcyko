from socketio.server import SocketIOServer
import werkzeug.serving
from gevent import monkey
import click

from angular_flask import app, socketio


def run_server(use_app=app, port=5000):
    SocketIOServer(('',port),use_app,resource="socket.io").serve_forever()

def run_debug_server(use_app=app, port=5000):
    SocketIOServer(('',port),use_app,resource="socket.io").serve_forever()

@click.command()
@click.option('--config',default="p", type=click.Choice(['p','d','t']), help='Type of Configuration')
@click.option('--port',default=5000, help='The Port the webserver should run on')
def configure(config, port):
    if config == "p":
        app.config.from_object('angular_flask.settings.ProductionConfig')
    elif config == "d":
        app.config.from_object('angular_flask.settings.DevelopmentConfig')
    elif config == "t":
        app.config.from_object('angular_flask.settings.TestingConfig')
    elif config == "n":
        pass
    monkey.patch_all()
    if config == "d":
        run_debug_server(app, port)
    else:
        run_server(app, port)



if __name__ == '__main__':
    configure()
