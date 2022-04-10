# iMPORTS #
# ------- #
import json
from unicodedata import category
from flask import Blueprint, jsonify, request
from api import db
from bson import ObjectId
from api.functions import send_result


test = Blueprint('test', __name__, template_folder='templates', static_folder='static')
test_collection = db.tests
question_collection = db.questions


# start a test
@test.route('/<category>/test', methods=['POST'])
def start_test(category):
    
    # query that the category exists on the backend
    question_collection.find({"category": category})
    
    test = test_collection.insert_one({
        "category": category,
        "completed": False,
    })
    test_ObjectId = test.inserted_id
    test_collection.find_one({"_id": test_ObjectId})
    test_id = str(test_ObjectId)
    return jsonify({'message': 'A new test has started!',
                    'test_id': test_id}), 201


# calculate the test's score
@test.route('/test/<test_id>/score', methods=['POST'])
def score_test(test_id):
    
    test_id = test_collection.find_one({"_id": ObjectId(test_id)})
    test_responses = request.get_json()
    
    values = []
    keys = []
    
    # calculate the score from the responses
    for key,value in test_responses.items():
        values.append(int(value))
         
        keys.append(str(key))
        no_of_keys = len(keys)
        
        score = sum(values)/(no_of_keys * 10) * 100
        
    # save score and update test status
    test_collection.update_one({"_id": test_id['_id']}, 
                               {
                                   "$set": 
                                   {
                                        "score": score,
                                        "completed": True,
                                   }})
    return jsonify({'score': score}), 200


@test.route('/test/<test_id>/result', methods=["POST"])
def get_result(test_id):
    
    test_id = test_collection.find_one({"_id": ObjectId(test_id)})
    
    score = test_id['score']
    test_category = test_id['category']
    email = request.json.get('email')
    name = request.json.get('name')
    
    # name and email in  lowercase
    lower_case_email = email.lower()
    lower_case_name = name.lower()
    
    # save name and email to db
    test_collection.update_one({"_id": test_id['_id']}, 
                               {
                                   "$set": 
                                   {
                                        "email": lower_case_email,
                                        "name": lower_case_name,
                                   }})
    email_subject = "Your test result"
    
    if test_category=="devops":
        email_category = "DevOps Engineer"
    elif test_category=="cloud":
        email_category = "Cloud Engineer"
    elif test_category=="product-design":
        email_category = "Product Designer"
        
    send_result(to_email=lower_case_email, subject=email_subject, score=score, name=name, template="result.html", category=email_category)
    return jsonify(score, "Result sent successfully")
