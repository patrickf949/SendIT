"""
Creates application
"""
import datetime
from flask import jsonify, Flask, request, Response, render_template
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_raw_jwt
    )
from flask_cors import CORS
from Application.controllers.validate import Validation


def create_app(config):
    """
    Creates flask Application
    params: configuration for current environment
    """
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['JWT_SECRET_KEY'] = 'Don-t-you-test-125'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

    Validation.dbname = config.dbname
    Validation.hostname = config.hostname

    CORS(app)
    jwt = JWTManager(app)
    blacklist = set()
    @app.route("/")
    def kingslanding():
        return jsonify([
            "SendIT!"
            +" SendIT is a courier service that helps users deliver parcels to"+
            " different destinations."+
            " SendIT provides courier quotes based on weight categories.",
            {
                "/api/v2/auth/signup | POST" : "User Sign up",
                "/api/v2/auth/login | POST" : "User Login",
                "/api/v2/parcels | POST" : "Create parcel",
                "/api/v2/parcels | GET" :  "Fetch all parcels",
                "/api/v2/parcel/<int:parcelId> | GET" : "fetch parcel by id",
                "/api/v2/parcels/<int:parcelId>/cancel | GET" : "Cancel a par"+
                "cel delivery order",
                "/api/v2/users | GET" : "View all users",
                "/api/v2/users/<int:userId>/parcels | GET" : "Fetch parcels by"+
                " a specific user - admin",
                "/api/v2/parcels/<int:parcelId>/destination | PUT" : "Update "+
                "a parcel delivery order's destination",
                "/api/v2/parcels/<int:parcelId>/presentLocation | PUT" :
                "Update the present location of a parcel delivery order",
                "/api/v2/parcels/<int:parcelId>/status | PUT" : "Update the sta"
                +"tus of a parel delivery order's destination",
            }
        ]), 200


    @app.route("/api/v2/logout", methods=['POST'])
    @jwt_required
    def logout():
        """
        logout user and dismiss refresh token
        """
        response = jsonify({'logged out':True})
        unique_identifier = get_raw_jwt()['jti']
        blacklist.add(unique_identifier)
        return response, 200


    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        unique_identifier = decrypted_token['jti']
        return unique_identifier in blacklist


    from Application.views import parcels_view, users_view

    app.register_blueprint(parcels_view.blue_print)
    app.register_blueprint(users_view.blue_print)

    return app
