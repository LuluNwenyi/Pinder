# iMPORTS #
# ------- #
import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from .config import env_config

# app config
app = Flask(__name__)
app.config['MONGO_URI'] = os.environ.get('MONGODB_URI')

mongo = PyMongo(app)
jwt = JWTManager()
bcrypt = Bcrypt()

# database config
db = mongo.db

# app factory
def create_app(config_name):
    
    app.config.from_object(env_config[config_name])

    mongo.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # blueprints
    from api.default import default as default_blueprint
    from api.admin.routes import admin as admin_blueprint
    from api.auth.routes import auth as auth_blueprint
    from api.questions.routes import questions as question_blueprint
    from api.quiz.routes import test as test_blueprint
    
    app.register_blueprint(default_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(question_blueprint)
    app.register_blueprint(test_blueprint)
    
    return app
