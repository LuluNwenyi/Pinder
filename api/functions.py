# iMPORTS #
# ------- #
from flask import jsonify, current_app, render_template, url_for
from flask_jwt_extended import get_jwt_identity
from itsdangerous import URLSafeTimedSerializer
from bson import ObjectId
from api import db

import os
import requests

admin_collection = db.admins
url = "https://api.mailgun.net/v3/results.mypinder.com/messages"

def send_result(to_email, subject, template, score, name, category):
    requests.post(
		url,
		auth=("api", os.environ.get("MAILGUN_API_KEY")),
		data={"from": os.environ.get("MAILGUN_FROM"),
			    "to": to_email,
			    "subject": subject,
			    "html": render_template(template, score=score, name=name, category=category)
       }
    )
    
def send_email(to_email, subject, action_url, template, name):
    requests.post(
        url,
        auth=("api", os.environ.get("MAILGUN_API_KEY")),
        data={"from": os.environ.get("MAILGUN_FROM"),
              "to": to_email,
              "subject": subject,
              "html": render_template(template, action_url=action_url)
              }
    )

def generate_confirmation_token(email):

    user = admin_collection.find_one({"email": email})

    # GENERATE TOKEN
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

    # SEND EMAIL
    subject = "Confirm Your Email Address"
    confirm_url = url_for("auth.confirm_email", token=token,  _external=True)
    user_name = user['name']

    send_email(to_email=email, subject=subject, action_url=confirm_url, template='confirmation.html', name=user_name)
    return jsonify({ "msg": "succesfully sent the confirmation mail to your email"}), 200

