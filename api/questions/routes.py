# iMPORTS #
# ------- #
from flask import Blueprint, jsonify, request
from api import db
from api.decorators import admin_required
from flask_jwt_extended import jwt_required

questions = Blueprint('questions', __name__)
question_collection = db.questions


#create a question
@questions.route('/question', methods=['POST'])
@jwt_required()
@admin_required
def create_question():
    
    # get question data from request
    question = request.json.get('question')
    category = request.json.get('category')
    option_1 = request.json.get('option_1')
    option_1_value = request.json.get('option_1_value')
    option_2 = request.json.get('option_2')
    option_2_value = request.json.get('option_2_value')
    option_3 = request.json.get('option_3')
    option_3_value = request.json.get('option_3_value')
    option_4 = request.json.get('option_4')
    option_4_value = request.json.get('option_4_value')

    # make sure question and category are provided
    if not question:
        return jsonify({'message': 'Please enter a question'}), 400
    if not category:
        return jsonify({'message': 'Please enter a category'}), 400
    
    # make sure at least 2 options are provided
    if not option_1:
        return jsonify({'message': 'Please enter at least 2 options'}), 400
    if not option_1_value:
        return jsonify({'message': 'Please set a value for this option'}), 400
    if not option_2:
        return jsonify({'message': 'Please enter at least 2 options'}), 400
    if not option_2_value:
        return jsonify({'message': 'Please set a value for this option'}), 400

    # add to database
    question_collection.insert_one({
        "question": question,
        "category": category,
        "option_1": option_1,
        "option_1_value": option_1_value,
        "option_2": option_2,
        "option_2_value": option_2_value,
        "option_3": option_3,
        "option_3_value": option_3_value,
        "option_4": option_4,
        "option_4_value": option_4_value
    })
        
    return jsonify({'message': 'Question created successfully'}), 200

