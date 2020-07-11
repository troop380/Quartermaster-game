from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import os

socketio = SocketIO()
db = SQLAlchemy()     


def create_app(debug=False,redishost='localhost'):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    db.init_app(app)
    #db_setup(db)
    #app.config['qmdb.room_members'] = db_setup(db)

    socketio.init_app(app)

    with app.app_context():
        db.create_all()
        return app
