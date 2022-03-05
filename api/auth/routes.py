# iMPORTS #
# ------- #
import datetime
from datetime import timedelta
from flask import Blueprint, jsonify, request
from api import db, bcrypt, jwt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, create_refresh_token, get_jwt_identity

auth = Blueprint('auth', __name__)
admin_collection = db.admins


# user login
@auth.route("/login", methods=["POST"])
def login_user():

    # query if the user exists
    existing_user = admin_collection.find_one({"email": request.json['email']})

    if existing_user:

        if existing_user and bcrypt.check_password_hash(existing_user['password'], request.json['password']):

            user_id = str(existing_user['_id'])

            token = create_access_token(identity=user_id, fresh=True, expires_delta=timedelta(minutes=30))
            refresh_token = create_refresh_token(identity=user_id, expires_delta=timedelta(hours=1))
            login_time = datetime.datetime.now()
            db.admins.update_one({"_id": existing_user['_id']}, {"$set": {"last_login": login_time}})

            return jsonify({"token": token,
                            "refresh_token": refresh_token}), 200

        else:
            response = {
                "message": "Incorrect password"
            }
            return jsonify(response), 401

    else:
        # if user doesn't exist
        response = {
            'message' : 'This user does not exist.'
        }
        return jsonify(response), 404


# refresh token
@auth.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():

    user_id = get_jwt_identity()
    new_token = create_access_token(identity=user_id, fresh=False)
    return jsonify({"token": new_token}), 200


# logout user
@auth.route("/logout", methods=["DELETE"])
@jwt_required()
def logout_user():

    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        token = db.tokens.find_one({"jti": jti})
        return token is not None

    jti = get_jwt()['jti']
    now = datetime.datetime.utcnow()
    db.tokens.insert_one({
        "jti": jti,
        "created_at": now
    })

    response = {
        "message": "User logged out successfully"
    }
    return jsonify(response), 200


# test authentication
@auth.route("/test", methods=["GET"])
@jwt_required()
def test_protection():
    
    response = {
        "message": "You are authorized"
    }
    return jsonify(response), 200


