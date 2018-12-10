from flask import request, Blueprint
from Application.models.parcels import Parcels
from Application.models.users import Users
from Application.controllers.validate import Validation
from flask_jwt_extended import jwt_required, get_jwt_identity


blue_print = Blueprint("Parcels", __name__)

response = Validation()

@blue_print.route('/api/v2/parcels/<int:parcel_id>')
@jwt_required
def getParcel(parcel_id):
    """
    Get parcel by id
    params: parcel id	
    returns: specified parcel
    """
    current_user = get_jwt_identity()
    return response.validate_get_parcel_by_id(current_user, parcel_id)


@blue_print.route ('/api/v2/parcels', methods=['GET','POST'])
@jwt_required
def addParcel():
    """	
    Create a parcel delivery order
    params: n/a
    returns: created parcel
    """
    current_user = get_jwt_identity()
    if request.method == 'POST':
        data = request.get_json()
        return response.validate_parcel_addition(current_user, data)
    elif request.method == 'GET':
        if not response.is_admin(current_user):
            user_id = response.get_user_id(current_user)
            return response.get_parcels_by_user_id(user_id)
        return response.validate_get_all_parcels(current_user)


@blue_print.route('/api/v2/users/<int:user_id>/parcels')
@jwt_required
def get_parcels_by_userId(user_id):
    """
    Gets all ids by a specified user id
    params: user id
    returns: specified user's parcels
    """
    current_user = get_jwt_identity()
    return response.validate_parcels_by_user(current_user, user_id)


@blue_print.route('/api/v2/users')
@jwt_required
def get_all_users():
    """
    gets all users in the system
    """
    current_user = get_jwt_identity()
    return response.validate_get_all_users(current_user)


@blue_print.route('/api/v2/parcel/categories')
@jwt_required
def get_weight_categories():
    """
    Get all weight categories for a logged in user
    """
    current_user = get_jwt_identity()
    return response.weight_categories(current_user)

@blue_print.route('/api/v2/parcels/<int:parcel_id>/destination', methods=['PUT'])
@jwt_required
def change_destination(parcel_id):
    """
    Change destination of parcel delivery order - user
    """
    current_user = get_jwt_identity()
    data = request.get_json()
    return response.validate_change_destination(current_user, parcel_id, data)

@blue_print.route('/api/v2/parcels/<int:parcel_id>/presentLocation', methods=['PUT'])
@jwt_required
def change_presentlocation(parcel_id):
    """
    Change present location of parcel delivery order - admin
    """
    current_user = get_jwt_identity()
    data = request.get_json()
    return response.validate_change_present_location(current_user, parcel_id, data)

@blue_print.route('/api/v2/parcels/<int:parcel_id>/status', methods=['PUT'])
@jwt_required
def change_status(parcel_id):
    """
    Change status of a parcel delivery order-admin
    params:parcel id
    returns: edited parcel
    """
    current_user = get_jwt_identity()
    data = request.get_json()
    return response.validate_change_status(current_user, parcel_id, data)
