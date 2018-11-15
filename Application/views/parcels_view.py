from flask import jsonify,Flask,request, Blueprint
from datetime import datetime
from Application.models import parcels
from Application.models import validate

blue_print = Blueprint("Parcels",__name__)

parcels =[
    {
        'parcel_id':1,
        'parcel_description':'Pumped Up Kicks & pinnata',
        'user_id':1,
        'client': 'BUcky',
        'recipient':'Mart',
        'pickup_location':'Quality Shopping Village',
        'destination':'Andela Uganda,Kira Road',
        'time_created':2018-9-11,
        'current_location':'Tuskys, Ntinda',
        'status':'Pending'
    }
]
admin_accounts=[]
user_accounts=[]
current_user =[]#store current user id
current_admin =[]#store current admin id

def logout_active_users():
    current_admin.pop()
    current_user.pop()

@blue_print.route('/api/v1/admin/signup',methods = ['POST'])
def admin_signup():
    #logout_active_users()
    data = request.get_json()
    
    admin_id=len(admin_accounts)+1
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if type(username)!=str or type(email) !=str or type(password)!=str:
        return jsonify({
            'message':'sorry! All fields must be strings'
        }),400

    if not username or username.isspace():
        return jsonify({
            'message':'sorry! your username is required and can not be an empty string'
        }), 400

    if not email or email.isspace():
        return jsonify({
            'message':'sorry! email is required and can not be an empty string'
        }), 400

    if not password or password.isspace():
        return jsonify({
            'message':'sorry! your password is required and can not be an empty string'
        }), 400

    admin =dict(
        admin_id =admin_id,
        username = username,
        email = email,
        password = password
    )
    
    admin_accounts.append(admin)

    return jsonify({
        'message': 'hello! '+admin['username']+' You Account has been created and automatically logged in',
    }),200

@blue_print.route('/api/v1/admin/login', methods = ['POST'])
def admin_login():
    if len(admin_accounts)==0:
        return jsonify({
            'message':'No accounts available yet'
        }),400
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')

    i=0#keeps track of admin index
    for existing_account in admin_accounts:
        if email==existing_account['email']:#if email exists
            if password==existing_account['password']:#if password matches
                current_admin.append(i)#store id of loggedin admin
                return jsonify({
                    'message':'Hello! '+existing_account['username']+' You are logged in'
                }),200
            return jsonify({
                'message':'Invalid email or password'
            }),400
        i+=1 
    
@blue_print.route('/api/v1/signup', methods = ['POST'])
def signup():
    
    data = request.get_json()
    user_id = len(user_accounts)+1
    username = data.get('username')
    email = data.get('email')
    password =data.get('password')

    if type(username)!=str or type(email)!=str or type(password)!=str:
        return jsonify({
            'message':'All information should be a sequence of characters(String type)'
        }),400
    
    if not username or not email or not password:
        return jsonify({
            'message':'Information missing, make sure username,email and password are passed'
        }),400
    
    if username.isspace() or email.isspace() or password.isspace():
        return jsonify({
            'message':'make sure all fields have information. no field can be an empty space'
        }),400
    
    for existing_account in user_accounts:
        if existing_account['email']==email:
            return jsonify({
                'message':'Email already exists'
            }),400

    user = dict(
        user_id =user_id,
        username=username,
        email=email,
        password=password
    )
    current_user.append(user_id)
    user_accounts.append(user)
    return jsonify({
        'message':'user has been added and logged in'
    })
    
@blue_print.route('/api/v1/login',methods=['POST'])
def login():
    logout_active_users()
    data = request.get_json()
    
    
    email = data.get('email')
    password =data.get('password')

    if type(email)!=str or type(password)!=str:
        return jsonify({
            'message':'All information should be a sequence of characters(String type)'
        }),400
    
    if not email or not password:
        return jsonify({
            'message':'Information missing, make sure username,email and password are passed'
        }),400
    
    if email.isspace() or password.isspace():
        return jsonify({
            'message':'make sure all fields have information. no field can be an empty space'
        }),400
    
    i=0
    for existing_account in user_accounts:
        if existing_account['email']==email:
            if existing_account['password']==password:
                current_user.append(i)
                return jsonify({
                    'message':existing_account['user']+'you are logged in'
                }),200
            return jsonify({
                'message':'invalid email or password'
            }),400
        i+=1

    return jsonify({
        'message':'Invalid email address or password'
    }),400
   

@blue_print.route('/api/v1/parcels')
def getParcels():
    if len(parcels)>0:
        return jsonify({
        'parcels':parcels
        }),200
    return jsonify({
        'message':'No parcels added yet'
    }),400

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
    if len(parcels)==0:
        return jsonify({
            'message':'No parcels yet'
        }),400
    elif parcel_id>len(parcels):
        return jsonify({
            'message':'Parcel does not exist'
        })
    
    parcels[parcel_id-1]['status']='canceled'
    return jsonify({
        'message':'Parcel status has been changed to canceled',
        'Parcel':parcels[parcel_id-1]
    })



@blue_print.route('/api/v1/users/<int:userId>/parcels')
def get_parcels_by_userId(user_id):
    """
    Gets all ids by a specified user id
    params: user id
    returns: specified user's parcels
    """
    if len(current_admin)==0:
        return jsonify({
            'message':'You are not logged in as admin'
        }),400
    if len(user_accounts)==0:
        return jsonify({
            'message':'No clients in the system yet'
        }),400
    if user_id>len(user_accounts):
        return jsonify({
            'message':'No client has the id you requested'
        }),400

    user_parcels=[]
    for parcel in parcels:
        if parcel['user_id']==user_id:
            user_parcels.append(parcel)
    if len(user_parcels)==0:
        return jsonify({
            "message":user_accounts[user_id-1]['username']+" has no parcels yet"
        })

    return jsonify({
        "message":user_accounts[user_id-1]['username']+"'s parcels",
        "parcels":user_parcels
    })


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

    