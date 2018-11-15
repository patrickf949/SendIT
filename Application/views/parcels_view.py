from flask import jsonify,Flask,request, Blueprint
from datetime import datetime
from Application.models import parcels
from Application.models import validate

blue_print = Blueprint("Parcels",__name__)

parcels =[
    {
        'parcel_id':1,
        'parcel_description':'Pumped Up Kicks & pinnata',
        'client': 'BUcky',
        'recipient':'Mart',
        'pickup_location':'Quality Shopping Village',
        'destination':'Andela Uganda,Kira Road',
        'time_created':2018-9-11,
        'current_location':'Tuskys, Ntinda',
        'status':'Pending'
    }
]
admin=[]
users=[]
current_user =[]#store current user id
current_admin =[]#store current admin id


@blue_print.route('/api/v1/admin/signup',methods = ['POST'])
def admin_signup():
    data = request.get_json()

    

@blue_print.route('/api/v1/parcels')
def getParcels():
   return jsonify({
       'parcels':parcels
   })

@blue_print.route('/api/v1/parcels/<int:parcel_id>')
def getParcel(parcel_id):
    """
    Get parcel by id
    params: parcel id
    returns: specified parcel
    """
    if len(parcels)==0:
        return jsonify({
            'message':'No Parcel delivery orders yet'
        }),205
    if not parcel_id or parcel_id < 1 or type(parcel_id)!=int:
        return jsonify({
            'message': 'sorry! book ID is required and can not be less than 1'
        }), 400
    for parcel in parcels:
        if parcel['parcel_id'] == parcel_id:
            return jsonify({
                'Specified parcel':parcel
            }), 200
    return jsonify({
        'message':'the book was not found'
    }), 205

@blue_print.route ('/api/v1/parcels', methods = ['POST'])
def addParcel():
    """
    Create a parcel delivery order
    params: n/a
    returns: created parcel
    """
    data = request.get_json()
    
    parcel_id=len(parcels)+1
    parcel_description = data.get('parcel_description')
    client = data.get('client')
    recipient = data.get('recipient')
    pickup_location = data.get('pickup_location')
    destination =data.get('destination')
    status='pending'
    if not parcel_description or parcel_description.isspace():
        return jsonify({
            'message':'sorry! the parcel_description is required and can not be an empty string'
        }), 400

    if not client or client.isspace():
        return jsonify({
            'message':'sorry! the client is required and can not be an empty string'
        }), 400

    if not recipient or recipient.isspace():
        return jsonify({
            'message':'sorry! the recipient is required and can not be an empty string'
        }), 400

    if not pickup_location or pickup_location.isspace():
        return jsonify({
            'message':'sorry! the pickup_location is required and can not be an empty string'
        }), 400

    

    parcel =dict(
        parcel_id=parcel_id,
        parcel_description = parcel_description,
        client = client,
        recipient = recipient,
        pickup_location = pickup_location,
        destination =destination,
        status = status
    )
    
    parcels.append(parcel)

    return jsonify({
        'message': 'hello! '+parcels[-1]['client']+' Your Parcel Delivery order has been placed',
        'Parcel':parcels[-1]
    }),200

@blue_print.route('/api/v1/parcels/<int:parcel_id>/update', methods = ['PUT'])
def updateParcel(parcel_id):
    """
    Update a specific parcel delivery order
    params: parcel_id
    returns: updated parcel 
    """
    data = request.get_json()
    
    parcel_description = data.get('parcel_description')
    client = data.get('client')
    recipient = data.get('recipient')
    pickup_location = data.get('pickup_location')
    destination =data.get('destination')
    status = 'pending'
    

    if not parcel_description or parcel_description.isspace():
        return jsonify({
            'message':'sorry! the parcel_description is required and can not be an empty string'
        }), 400

    if not client or client.isspace():
        return jsonify({
            'message':'sorry! the client is required and can not be an empty string'
        }), 400

    if not recipient or recipient.isspace():
        return jsonify({
            'message':'sorry! the recipient is required and can not be an empty string'
        }), 400

    if not pickup_location or pickup_location.isspace():
        return jsonify({
            'message':'sorry! the pickup_location is required and can not be an empty string'
        }), 400

    
    parcel_index =parcel_id-1
    
    status =parcels[parcel_index]['status']
    parcel =dict(
        parcel_id=parcel_id,
        parcel_description = parcel_description,
        client = client,
        recipient = recipient,
        pickup_location = pickup_location,
        destination =destination,
        status=status
    )
    del parcels[parcel_index]
    parcels.insert(parcel_index,parcel)
    return jsonify({
        'Message': 'Parcel has been Updated',
        'parcel': parcel
    }),200

        
    

@blue_print.route('/api/v1/parcels/<int:parcelId>/cancel')
def cancel_delivery_order(parcel_id):
    """
    Cancel a delivery order
    params: parcelid
    returns: cancelled delivery order
    """
    parcels[parcel_id-1]['status']='canceled'



@blue_print.route('/api/v1/users/<int:userId>/parcels')
def get_parcels_by_userId(user_id):
    """
    Gets all ids by a specified user id
    params: user id
    returns: specified user's parcels
    """
    pass

# def validation(parcel_description,client, recipient, pickup_location,Destination):
#     if not parcel_description or parcel_description.isspace():
#         return jsonify({
#             'message':'sorry! the parcel_description is required and can not be an empty string'
#         }), 400

#     if not client or client.isspace():
#         return jsonify({
#             'message':'sorry! the client is required and can not be an empty string'
#         }), 400

#     if not recipient or recipient.isspace():
#         return jsonify({
#             'message':'sorry! the recipient is required and can not be an empty string'
#         }), 400

#     if not pickup_location or pickup_location.isspace():
#         return jsonify({
#             'message':'sorry! the pickup_location is required and can not be an empty string'
#         }), 400

    