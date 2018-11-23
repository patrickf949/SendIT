import datetime
from flask import jsonify, Flask, request
from flask_jwt_extended import (
    jwt_required, create_access_token,
    create_refresh_token, get_jwt_identity,
    )
from Application.controllers.validate import Validation


def create_app(config):

    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'Don-t-you-test-125'
    Validation.dbname = config.dbname

    @app.route("/")
    def kingslanding():
        return jsonify([
            "SendIT!"
            +"SendIT is a courier service that helps users deliver parcels to different destinations."
            +" SendIT provides courier quotes based on weight categories.",
            {
                "/api/v2/auth/signup | POST" : "User Sign up",
                "/api/v2/auth/login | POST" : "User Login",
                "/api/v2/parcels | POST" : "Create parcel",
                "/api/v2/parcels | GET" :  "Fetch all parcels",
                "/api/v2/parcel/<int:parcelId> | GET" : "fetch parcel by id",
                "/api/v2/parcels/<int:parcelId>/cancel | GET" : "Cancel a parcel delivery order",
                "/api/v2/users | GET" : "View all users",
                "/api/v2/users/<int:userId>/parcels | GET" : "Fetch parcels by a specific user",
                "/api/v2/parcels/<int:parcelId>/destination | PUT" : "Update a parcel delivery order's destination",
                "/api/v2/parcels/<int:parcelId>/presentLocation | PUT" : "Update the present location of a parcel delivery order",
                "/api/v2/parcels/<int:parcelId>/status | PUT" : "Update the status of a parel delivery order's destination",
            }
        ])


    @app.route("/api/v2/logout", methods=['POST'])
    def logout():
        """
        logout user and dismiss refresh token
        """
        response = jsonify({'logged out':True})

        return response, 200


    @app.route('/api/v2/auth/signup', methods=['POST'])
    def signup():
        data = request.get_json()
        response = Validation()
        return response.validate_signup(data)


    @app.route('/api/v2/auth/login', methods=['POST'])
    def login():
        response = Validation()
        data = request.get_json()
        logged_in = response.validate_user_login(data)
        if logged_in == True:
            username = data.get('username')
            access_token = create_access_token(
                identity=username, 
                expires_delta=datetime.timedelta(days=1)
            )
            response = jsonify({'login':True})
            return jsonify({
                'message':'Hello '+username+' you are logged into SendIT',
                'Access_token':access_token
                }), 200
        return logged_in

    from Application.views import parcels_view
    app.register_blueprint(parcels_view.blue_print)

    return app