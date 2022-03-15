# iMPORTS #
# ------- #
import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from flask_mailgun import Mailgun
from flask_bcrypt import Bcrypt
from .config import env_config

TEMPLATE_DIR = os.path.abspath('templates')
STATIC_DIR = os.path.abspath('static')

# app config
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.config['MONGO_URI'] = os.environ.get('MONGODB_URI')
app.config['MAILGUN_DOMAIN'] = os.environ.get('MAILGUN_DOMAIN')
app.config['MAILGUN_API_KEY'] = os.environ.get('MAILGUN_API_KEY')

mongo = PyMongo(app)
jwt = JWTManager()
bcrypt = Bcrypt()
mailgun = Mailgun()

# database config
db = mongo.db

# app factory
def create_app(config_name):
    
    app.config.from_object(env_config[config_name])

    mongo.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    mailgun.init_app(app)

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
