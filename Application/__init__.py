import datetime
from flask import jsonify, Flask, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, jwt_refresh_token_required,
    create_refresh_token, get_jwt_identity,
    )
from Application.controllers.validate import Validation


def create_app(config):

    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'Don-t-you-test-125'
    Validation.dbname = config.dbname

    jwt = JWTManager(app)

    @app.route("/")
    def kingslanding():
        return jsonify([
            "SendIT!"
            +"SendIT is a courier service that helps users deliver parcels to different destinations."
            +" SendIT provides courier quotes based on weight categories.",
            {
                "/api/v2/signup | POST" : "User Sign up",
                "/api/v2/login | POST" : "User Login",
                "/api/v2/parcels | POST" : "Create parcel",
                "/api/v2/signup | POST" : "Create parcel",
                "/api/v2/parcels | GET" :  "Fetch all parcels",
                "/api/v2/parcel/<int:parcelId> | GET" : "fetch parcel by id",
                "/api/v2/parcels/<int:parcelId>/cancel | GET" : "Cancel a parcel delivery order",
                "/api/v2/users | GET" : "View all users",
                "/api/v2/users/<int:userId>/parcels | POST" : "Fetch parcels by a specific user",
                "/api/v2/parcels/<int:parcelId>/update | PUT" : "Update a parcel delivery order"
            }
        ])

    @app.route("/api/v2/refresh-token")
    @jwt_refresh_token_required
    def refresh_token():
        """
        Refresh tokens
        """
        logged_in_user = get_jwt_identity()
        access_token = create_access_token(identity=logged_in_user)

        response = jsonify({'refreshed':True}), 200


    @app.route("/api/v2/logout", methods=['POST'])
    def logout():
        """
        logout user and dismiss refresh token
        """
        response = jsonify({'logged out':True})

        return response, 200


    @app.route('/api/v2/signup', methods=['POST'])
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