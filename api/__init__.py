# iMPORTS
import os
import certifi
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from .config import config

# APP CONFiG
app = Flask(__name__)

mongo = PyMongo(app)
jwt = JWTManager()
bcrypt = Bcrypt()

# APP FACTORY
def create_app(config_name):

    # INIT APP CONFiG IN APP
    app.config.from_object(config[config_name])

    # INIT APP IN MANAGERS
    mongo.init_app(app, uri=os.environ.get('MONGODB_URI'), connectTimeoutMS=30000, socketKeepAlive=True, connect=False, maxPoolsize=1, tlsCAFile=certifi.where())
    jwt.init_app(app)
    bcrypt.init_app(app)

    # REGISTRATION OF BLUEPRINTS
    from api.main import default as default_blueprint
    
    app.register_blueprint(default_blueprint)
    
    return app