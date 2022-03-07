# iMPORTS #
# ------- # 
import datetime
from flask import Blueprint, jsonify, request
from api import db, bcrypt
from bson import ObjectId
from api.decorators import admin_required
from flask_jwt_extended import jwt_required

admin = Blueprint('admin', __name__)
admin_collection = db.admins

@admin.route('/create-admin', methods=['POST'])
def create_admin():
    
    # query for user
    existing_user = admin_collection.find_one({"email": request.json['email']})

    if not existing_user:

        try:
            # register the user
            password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
            email = request.json['email']
            name = request.json['name']
            admin_collection.insert_one({
                                    "name": name,
                                    "email": email,
                                    "password": password,
                                    "admin": True,
                                    "confirmed_email": False,
                                    "created_at": datetime.datetime.utcnow(),
                                    "confirmed_at": None,
                                    "last_login": datetime.datetime.utcnow(),
            })
            
            #generate_confirmation_token(email)
            return jsonify({"message": "User created successfully"}), 201
            
        except Exception as e:
            return jsonify({'message': str(e)}), 500
        
    else:
        # if user exists
        response = {
            'message' : 'This user already exists.'
        }
        return jsonify(response), 409
        

# get all admins        
@admin.route('/admins', methods=['GET'])
@jwt_required()
@admin_required
def admin_list():
    
    all_admins = admin_collection.find({})
    admin_list = []
    
    for admin in all_admins:
        admin_data = {}
        admin_data["id"] = str(admin["_id"])
        admin_data["name"] = str(admin["name"])
        admin_data["email"] = str(admin["email"])
        
        admin_list.append(admin_data)
        
    return jsonify(admin_list), 200
        

#get one admin
@admin.route('/admin/<admin_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_admin(admin_id):
    
    admin = admin_collection.find_one({"_id": ObjectId(admin_id)})
    if not admin:
        return jsonify({'message': 'User not found'}), 404
    
    admin_data = {}
    admin_data["id"] = str(admin["_id"])
    admin_data["name"] = str(admin["name"])
    admin_data["email"] = str(admin["email"])
    
    return jsonify(admin_data), 200


# delete admin details       
@admin.route('/admin/<admin_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_admin(admin_id):
    
    admin = admin_collection.find_one({"_id": ObjectId(admin_id)})
    if admin:
        try:
            admin_collection.delete_one({"_id": ObjectId(admin_id)})
            return jsonify({'message': 'User deleted successfully'}), 200
        
        except Exception as e:
            return jsonify({'message': str(e)}), 500
        
    else:
        return jsonify({'message': 'User not found'}), 404    
