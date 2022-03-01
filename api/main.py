#----- IMPORTS -----#

from flask import Blueprint, jsonify

default = Blueprint('default', __name__)

# HOME PAGE
@default.route('/')
def index():

    return jsonify({"message":"Welcome to the Pomodoroll APi"})