import datetime
from flask import request, Blueprint, jsonify
from Application.models.parcels import Parcels
from Application.models.users import Users
from Application.controllers.validate import Validation
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_raw_jwt
    )
from Application import create_app

blue_print = Blueprint("Users", __name__)

response = Validation()


@blue_print.route('/api/v2/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()
    response = Validation()
    return response.validate_signup(data)


@blue_print.route('/api/v2/auth/login', methods=['POST'])
def login():
    """
    User logsin
    """
    response = Validation()
    data = request.get_json()
    logged_in = response.validate_user_login(data)
    if logged_in == True:
        username = data.get('username')
        
        access_token = create_access_token(
            identity=username, 
            expires_delta=datetime.timedelta(days=4000)
        )

        if not response.is_admin(username):
            return jsonify({
                'message':'Hello '+username+' you are logged into SendIT',
                'Access_token':access_token
                }), 200
        return jsonify({
                'message':'Hello '+username+' you are logged into SendIT as admin',
                'Access_token':access_token
                }), 200
    return logged_in
