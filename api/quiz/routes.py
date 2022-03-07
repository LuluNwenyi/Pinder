# iMPORTS #
# ------- #
from flask import Blueprint, jsonify, request
from api import db
from bson import ObjectId


test = Blueprint('test', __name__)
test_collection = db.tests
question_collection = db.questions

@test.route('/<category>/test', methods=['POST'])
def start_test(category):
    
    # get test data from request
    category = question_collection.find({"category": category})
    
    test_collection.insert_one({
        "category": "category",
        "completed": False,
    })
    
    return jsonify({'message': 'A new test has started!'}), 200


@test.route('/test/<test_id>/score', methods=['POST'])
def score_test(test_id):
    
    test_id = test_collection.find_one({"_id": ObjectId(test_id)})
    test_responses = request.get_json()
    values = []
    keys = []
    for key,value in test_responses.items():
        values.append(int(value))
         
        keys.append(str(key))
        no_of_keys = len(keys)
        
    print(sum(values), no_of_keys)
        
    #return jsonify(test_responses), 200
    return jsonify({'message': 'Still implementing this route'}), 200
