"""
Handles all validation
"""

from .parcels import Parcels
from flask import jsonify
from .users import Users

class Validation():
    #Handles all validation
    
    def validate_admin_signup(self,data):
        
    
        admin_id=len(Users.admin_accounts)+1
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        temp_user=[username,email,password]
        
        valid_data =self.validate_userdata(temp_user)

        if valid_data!=True:
            return valid_data

        admin =dict(
            admin_id =admin_id,
            username = username,
            email = email,
            password = password
        )
        
        Users.admin_accounts.append(admin)

        return jsonify({
            'message': 'hello! '+admin['username']+' You Account has been created and automatically logged in',
        }),200

    def validate_user_signup(self,data):
        
        user_id=len(Users.user_accounts)+1
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        temp_user=[username,email,password]
        
        valid_data =self.validate_userdata(temp_user)

        if valid_data!=True:
            return valid_data
        
        user =dict(
            user_id =user_id,
            username = username,
            email = email,
            password = password
        )
        
        Users.user_accounts.append(user)

        return jsonify({
            'message': 'hello! '+user['username']+' You Account has been created and automatically logged in',
        }),200


    def validate_userdata(self,temp_list):
        for element in temp_list:
            if type(element)!=str:
                return jsonify({
                'message':'sorry! All fields must be strings'
            }),400

            elif not element or element.isspace():
                return jsonify({
                'message':'sorry! your username is required and can not be an empty string'
            }), 400
        
        return True


    def validate_parcels_by_user(self,user_id):
        if len(Users.user_accounts)==0:
            return jsonify({
                'message':'No clients in the system yet'
            }),400
        if user_id>len(Users.user_accounts):
            return jsonify({
                'message':'No client has the id you requested'
            }),400

        user_parcels=[]
        for parcel in Parcels.parcels:
            if parcel['user_id']==user_id:
                user_parcels.append(parcel)
        if len(user_parcels)==0:
            return jsonify({
                "message":Users.user_accounts[user_id-1]['username']+" has no parcels yet"
            })

        return jsonify({
            "message":Users.user_accounts[user_id-1]['username']+"'s parcels",
            "parcels":user_parcels
        })
    
    def validate_cancel_parcel_delivery_order(self,parcel_id):
        if len(Parcels.parcels)==0:
            return jsonify({
                'message':'No parcels yet'
            }),400
        elif parcel_id>len(Parcels.parcels):
            return jsonify({
                'message':'Parcel does not exist'
            }),400
        
        Parcels.parcels[parcel_id-1]['status']='canceled'
        return jsonify({
            'message':'Parcel status has been changed to canceled',
            'Parcel':Parcels.parcels[parcel_id-1]
        }),200


    def validate_update_parcel_delivery_order(self,data,parcel_id):
        parcel_exists =self.check_if_parcel_id_exists(parcel_id)
        if parcel_exists!=True:
            return parcel_exists
        parcel_description = data.get('parcel_description')
        recipient = data.get('recipient')
        pickup_location = data.get('pickup_location')
        destination =data.get('destination')        

        if not parcel_description or parcel_description.isspace():
            return jsonify({
                'message':'sorry! the parcel_description is required and can not be an empty string'
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
        
        Parcels.parcels[parcel_index]['parcel_description'] = parcel_description
        Parcels.parcels[parcel_index]['recipient'] = recipient
        Parcels.parcels[parcel_index]['pickup_location'] = pickup_location
        Parcels.parcels[parcel_index]['destination'] =destination
        
        
        
        return jsonify({
            'Message': 'Parcel has been Updated',
            'parcel': Parcels.parcels[parcel_index]
        }),200
    
    def validate_parcel_addition(self,data):
        
        
        parcel_id=len(Parcels.parcels)+1
        parcel_description = data.get('parcel_description')
        client = data.get('client')
        user_id=self.get_user_id(client)
        recipient = data.get('recipient')
        pickup_location = data.get('pickup_location')
        destination =data.get('destination')
        status='pending'
        temp_parcel = [parcel_description,client,recipient,pickup_location,destination]

        if user_id is False:
            return jsonify({
                    'message':'Create an account first'
                }),400
        for element in temp_parcel:
            if type(element)!=str:
                return jsonify({
                    'message':'All specifications should be a sequence of characters'
                }),400

            elif not element or element.isspace():
                return jsonify({
                    'message':'All your specifications should be available and should not be a space. Make sure you have the following',
                    '1. ':'parcel description',
                    '2. ':'recipient',
                    '3. ':'recipients contact',
                    '4. ':'pickup location',
                    '5. ':'destination'
                }),400

        parcel =dict(
            parcel_id=parcel_id,
            parcel_description = parcel_description,
            client = client,
            user_id=user_id,
            recipient = recipient,
            pickup_location = pickup_location,
            destination =destination,
            status = status
        )
        

        Parcels.parcels.append(parcel)

        return jsonify({
            'message': 'hello! '+Parcels.parcels[-1]['client']+' Your Parcel Delivery order has been placed',
            'Parcel':Parcels.parcels[-1]
        }),200
    


    def validate_get_parcel_by_id(self,parcel_id):
        if self.check_if_parcel_id_exists(parcel_id)!=True:
            return self.check_if_parcel_id_exists(parcel_id)
            
        for parcel in Parcels.parcels:
            if parcel['parcel_id'] == parcel_id:
                return jsonify({
                    'Specified parcel':parcel
                }), 200

        return jsonify({
            'message':'the parcel was not found'
        }), 400
    

    def validate_get_all_parcels(self):
        if len(Parcels.parcels)>0:
            return jsonify({
            'parcels':Parcels.parcels
            }),200

        return jsonify({
            'message':'No parcels added yet'
        }),400

    
    def get_user_id(self,client):
        
        for user in Users.user_accounts:
            if user['username']==client:
                user_id = user['user_id']
                return user_id

        return False
    

    def validate_get_all_users(self):

        if len(Users.user_accounts)>0:
            return jsonify({
                'Users':Users.user_accounts
            }),200

        return jsonify({
            'message':'No users in the system'
        }),400
    
    def check_if_parcel_id_exists(self,parcel_id):
        if len(Parcels.parcels)==0:
            return jsonify({
                'message':'No parcel delivery orders'
            }),400
        
        if parcel_id>len(Parcels.parcels) or parcel_id==0:
            return jsonify({
                'message':'invalid parcel id'
            }),400

        return True