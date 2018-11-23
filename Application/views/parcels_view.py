from flask import jsonify,Flask,request, Blueprint
from Application.models.parcels import Parcels
import Application
from Application.models.users import Users
from Application.controllers.validate import Validation
from flask_jwt_extended import jwt_required,get_jwt_identity


blue_print = Blueprint("Parcels",__name__)

response = Validation()

@blue_print.route('/api/v2/parcels/<int:parcel_id>')
@jwt_required
def getParcel(parcel_id):
    """
    Get parcel by id
    params: parcel id	
    returns: specified parcel
    """
    current_user = get_jwt_identity
    return response.validate_get_parcel_by_id(parcel_id,current_user)


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
        return response.validate_parcel_addition(current_user,data)
    elif request.method == 'GET':
        return response.validate_get_all_parcels(current_user)


@blue_print.route('/api/v2/parcels/<int:parcel_id>/update', methods=['PUT'])
@jwt_required
def updateParcel(parcel_id):
    """
    Update a specific parcel delivery order
    params: parcel_id
    returns: updated parcel 
    """
    data = request.get_json()
    current_user = get_jwt_identity()

    return response.validate_update_parcel_delivery_order(current_user, data, parcel_id)
    

@blue_print.route('/api/v2/parcels/<int:parcel_id>/cancel')
@jwt_required
def cancel_delivery_order(parcel_id):
    """
    Cancel a delivery order
    params: parcelid
    returns: cancelled delivery order
    """
    current_user = get_jwt_identity()
    print(current_user)
    return response.validate_cancel_parcel_delivery_order(current_user, parcel_id)


@blue_print.route('/api/v2/users/<int:user_id>/parcels')
@jwt_required
def get_parcels_by_userId(user_id):
    """
    Gets all ids by a specified user id
    params: user id
    returns: specified user's parcels
    """
    current_user = get_jwt_identity()
    return response.validate_parcels_by_user(current_user,user_id)


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

@blue_print.route('/api/v2/parcels/<int:parcelId>/destination', methods=['PUT'])
@jwt_required
def change_destination(parcel_id):
    """
    Change destination of parcel delivery order - user
    """
    current_user = get_jwt_identity()
    data = request.get_json()
    return response.weight_categories(current_user,parcel_id,data)

@blue_print.route('/api/v2/parcels/<int:parcelId>/presentLocation', methods=['PUT'])
@jwt_required
def change_presentlocation(parcel_id):
    """
    Change present location of parcel delivery order - admin
    """
    current_user = get_jwt_identity()
    data = request.get_json()
    return response.weight_categories(current_user,parcel_id,data)

@blue_print.route('/api/v2/parcels/<int:parcelId>/status', methods=['PUT'])
@jwt_required
def change_status(parcel_id):
    """
    Change status of a parcel delivery order-admin
    params:parcel id
    returns: edited parcel
    """
    current_user = get_jwt_identity()
    data = request.get_json()
    return response.weight_categories(current_user)