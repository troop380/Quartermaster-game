from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_session import Session
import os
from datetime import timedelta

socketio = SocketIO(manage_session=False)
db = SQLAlchemy()
login_manager = LoginManager()
sess = Session()

def create_app(debug=False,redishost='localhost'):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['SESSION_SQLALCHEMY'] = db
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    db.init_app(app)
    socketio.init_app(app)
    login_manager.init_app(app)
    sess.init_app(app)

    with app.app_context():
        db.create_all()
        return app
