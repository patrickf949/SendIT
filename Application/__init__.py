from flask import jsonify,Flask
from Application.models.database import Database

app = Flask(__name__)

def create_app(config):

    app = Flask(__name__)
    Database.dbname = config['dbname']
    @app.route("/")
    def kingslanding():
        return jsonify([
            "SendIT!"
            +"SendIT is a courier service that helps users deliver parcels to different destinations. SendIT provides courier quotes based on weight categories.",{
                "/api/v1/parcels":"Create parcel"
                ,"/api/v1/parcels": "Fetch all parcels"
                ,"/api/v1/parcel/<int:parcelId>": "fetch parcel by id"                
                ,"/api/v1/parcels/<int:parcelId>/cancel": "Cancel a parcel delivery order"
                ,"/api/v1/users": "View all users"
                ,"/api/v1/users/<int:userId>/parcels":"Fetch parcels by a specific user"
                ,"/api/v1/parcels/<int:parcelId>/update":"Update a parcel delivery order"
            }            
        ])

    
    from Application.views import parcels_view
    app.register_blueprint(parcels_view.blue_print)
    
    return app 