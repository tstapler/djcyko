from socketio.server import SocketIOServer
from angular_flask import app, socketio
from gevent import monkey
import click

@click.command()
@click.option('--config',default="p", type=click.Choice(['p','d','t']), help='Type of Configuration')
@click.option('--port',default=5000, help='The Port the webserver should run on')
def run_server(config, port):
    print(port)
    if config == "p":
        app.config.from_object('angular_flask.settings.ProductionConfig')
    elif config == "d":
        app.config.from_object('angular_flask.settings.DevelopmentConfig')
    elif config == "t":
        app.config.from_object('angular_flask.settings.TestingConfig')
    elif config == "n":
        pass

    monkey.patch_all()
    SocketIOServer(('',port),app,resource="socket.io").serve_forever()

if __name__ == '__main__':
    run_server()
