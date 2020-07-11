from flask import Flask
from flask_socketio import SocketIO
import redis
import argparse

socketio = SocketIO()

# initialize redis stuff
# Is there a better place to put this?
parser = argparse.ArgumentParser()
parser.add_argument('--redishost', type=str, default='localhost', help='optional redis server name')
args = parser.parse_args()
print("redis host {}".format(args.redishost))
rdata = redis.StrictRedis(host=args.redishost, port=6379, decode_responses=True)


def create_app(debug=False,redishost='localhost'):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    socketio.init_app(app)
    return app
