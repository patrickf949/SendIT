from flask import jsonify,Flask
from Application.controllers.database import Database
from Application.controllers.validators

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,jwt_refresh_token_required,
    create_refresh_token,get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
    )



def create_app(config):

    app = Flask(__name__)
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_SECURE'] = False
    app.config['JWT_COOKIE_PATH'] = '/cookiepath'
    app.config['JWT_REFRESH_COOKIE_PATH'] = '/me-cookie/fresh'
    app.config['JWT_COOKIE_CRSF_PROTECT'] = True
    app.config['JWT_SECRET_KEY'] = 'Don-t-you-test-125'


    @app.route("/")
    def kingslanding():
        return jsonify([
            "SendIT!"
            +"SendIT is a courier service that helps users deliver parcels to different destinations. SendIT provides courier quotes based on weight categories.",{
                "/api/v2/parcels":"Create parcel"
                ,"/api/v2/parcels": "Fetch all parcels"
                ,"/api/v2/parcel/<int:parcelId>": "fetch parcel by id"                
                ,"/api/v2/parcels/<int:parcelId>/cancel": "Cancel a parcel delivery order"
                ,"/api/v2/users": "View all users"
                ,"/api/v2/users/<int:userId>/parcels":"Fetch parcels by a specific user"
                ,"/api/v2/parcels/<int:parcelId>/update":"Update a parcel delivery order"
            }            
        ])

    
    from Application.views import parcels_view
    app.register_blueprint(parcels_view.blue_print)

    return app