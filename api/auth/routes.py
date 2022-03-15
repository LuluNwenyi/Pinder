# iMPORTS #
# ------- #
import datetime
from datetime import timedelta
from flask import Blueprint, abort, jsonify, request, current_app, url_for
from itsdangerous import URLSafeTimedSerializer
from api import db, bcrypt, jwt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, create_refresh_token, get_jwt_identity
from api.functions import send_email

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

# confirm email
@auth.route("/confirm_email/<token>", methods=["PATCH"])
def confirm_email(token):

    ts = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    email = ts.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=3600)

    user = admin_collection.find_one({"email": email})
    if user:
        admin_collection.update_many({"_id": user['_id']}, {"$set": {"confirmed_email": True, "confirmed_at": datetime.datetime.utcnow()}})
        response = {
            "message": "Email confirmed"
        }
        return jsonify(response), 200

    else:
        response = {
            'message' : 'This user does not exist.'
        }
        return jsonify(response), 404


# FORGOT PASSWORD ROUTE
@auth.route('/forgot-password', methods=['POST'])
def forgot_password():
    
    email = request.json['email']
    
    user = admin_collection.find_one({"email": email})
    if user:

        subject = "Reset Your Password"
        ts = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        token = ts.dumps(email, salt=current_app.config["SECURITY_PASSWORD_SALT"])
        recovery_url = url_for("auth.reset_password", token=token,  _external=True)

        send_email(to_email=email, subject=subject, template='password_reset.html', name=user['name'], action_url=recovery_url)
        return jsonify({ "msg": "succesfully sent the reset mail to your email"}), 200
    
    else:
        return jsonify({"message": "This user does not exist."}), 404


# RESET PASSWORD ROUTE
@auth.route('/reset/<token>', methods=['PATCH'])
def reset_password(token):

    ts = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    new_password = request.json['password']

    try:
        email = ts.loads(token, salt=current_app.config["SECURITY_PASSWORD_SALT"], max_age=3600)
    except:
        abort(404)

    if email is False:
        return jsonify({"message": "Invalid token or token expired"}), 401
    
    user = admin_collection.find_one({"email": email})   

    if not user:
        return jsonify({"message": "User not found"}), 404  

    if user:
        new_password_hash = bcrypt.generate_password_hash(new_password)
        admin_collection.update_one({"email": email}, {"$set": {"password": new_password_hash}})

        return jsonify({'message': 'Your password has been reset!'}), 200

    else:
        return {"message": "An error occured"},   400
