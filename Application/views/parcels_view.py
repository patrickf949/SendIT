from flask import jsonify,Flask,request, Blueprint
from datetime import datetime
from Application.models.parcels import Parcels
from Application.models.users import Users
from Application.controllers.validate import Validation
from flask_jwt_extended import jwt_required


blue_print = Blueprint("Parcels",__name__)

response = Validation()

@blue_print.route('/api/v2/admin/signup',methods = ['POST'])
def admin_signup():
    """
    Signup admin
    """
    data = request.get_json()
    return response.validate_signup(data,True)

    
@blue_print.route('/api/v2/signup', methods = ['POST'])
def signup():
    data = request.get_json()
    return response.validate_signup(data)


@blue_print.route('/api/v2/auth/login',methods = ['POST'])
def login():
    data = request.get_json()
    return response.validate_user_login(data)

@blue_print.route('/api/v2/auth/admin/login',methods = ['POST'])
def admin_login():
    data = request.get_json()
    return response.validate_user_login(data,True)

@blue_print.route('/api/v2/parcels')
@jwt_required
def getParcels():
    return response.validate_get_all_parcels()    

@blue_print.route('/api/v2/parcels/<int:parcel_id>')
@jwt_required
def getParcel(parcel_id):
    """
    Get parcel by id
    params: parcel id	
    returns: specified parcel
    """
    return response.validate_get_parcel_by_id(parcel_id)

@blue_print.route ('/api/v2/parcels', methods = ['POST'])
@jwt_required
def addParcel():
    """	
    Create a parcel delivery order
    params: n/a
    returns: created parcel
    """
    data = request.get_json()
    
    return response.validate_parcel_addition(data)

@blue_print.route('/api/v2/parcels/<int:parcel_id>/update', methods = ['PUT'])
@jwt_required
def updateParcel(parcel_id):
    """
    Update a specific parcel delivery order
    params: parcel_id
    returns: updated parcel 
    """
    data = request.get_json()
    
    return response.validate_update_parcel_delivery_order(data,parcel_id)

        
    

@blue_print.route('/api/v2/parcels/<int:parcel_id>/cancel')
@jwt_required
def cancel_delivery_order(parcel_id):
    """
    Cancel a delivery order
    params: parcelid
    returns: cancelled delivery order
    """
    
    return response.validate_cancel_parcel_delivery_order(parcel_id)



@blue_print.route('/api/v2/users/<int:user_id>/parcels')
@jwt_required
def get_parcels_by_userId(user_id):
    """
    Gets all ids by a specified user id
    params: user id
    returns: specified user's parcels
    """
    
    return response.validate_parcels_by_user(user_id)

@blue_print.route('/api/v2/users')
@jwt_required
def get_all_users():
    """
    gets all users in the system
    """
    return response.validate_get_all_users()

