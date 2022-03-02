# iMPORTS
import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from .config import env_config

# APP CONFiG
app = Flask(__name__)
app.config['MONGO_URI'] = os.environ.get('MONGODB_URI')

mongo = PyMongo(app)
jwt = JWTManager()
bcrypt = Bcrypt()

# APP FACTORY
def create_app(config_name):

    # INIT APP CONFiG IN APP
    app.config.from_object(env_config[config_name])

    # INIT APP IN MANAGERS
    mongo.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # REGISTRATION OF BLUEPRINTS
    from api.default import default as default_blueprint
    
    app.register_blueprint(default_blueprint)
    
    return app
