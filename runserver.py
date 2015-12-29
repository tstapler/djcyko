from socketio.server import SocketIOServer
from werkzeug.debug import DebuggedApplication
import werkzeug.serving
from gevent import monkey
import click

monkey.patch_all()
from angular_flask import app, socketio


def run_server(use_app=app, port=5000):
    SocketIOServer(('',port),use_app,resource="socket.io").serve_forever()

@werkzeug.serving.run_with_reloader
def run_debug_server(use_app=app, port=5000):
    app = DebuggedApplication(use_app, evalex=True)
    SocketIOServer(('',port),app,resource="socket.io").serve_forever()

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
    if config == "d":
        run_debug_server(app, port)
    else:
        run_server(app, port)



if __name__ == '__main__':
    configure()
