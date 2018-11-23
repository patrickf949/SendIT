"""
Handles all validation as well as manipulation
"""
from json import dumps
from flask import jsonify
from Application.models.users import Users
from Application.models.parcels import Parcels
import datetime
from .database import Database

class Validation():
    """
    All validation
    """
    dbname=''
    def __init__(self):
        self.database = Database(Validation.dbname)


    def validate_signup(self, data, admin=False):

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        contact =data.get('contact')
        
        temp_user = dict(
            username=username,
            email=email,
            password=password,
            contact=contact,
        )
        
        valid_data =self.validate_userdata(temp_user.copy())
        print(valid_data)
        if valid_data!=True:
            return valid_data

        user = temp_user
        user['admin'] = admin
        if not admin:
            self.database.add_user(user)
            return jsonify({
                'message': 'hello! '+user['username']+' Your Account has been created. Please login',
            }), 200
        else:
            self.database.add_user(user)
            return jsonify({
                'message': 'hello! '+user['username']+' Your Admin Account has been created. Please login',
            }), 200


    def validate_userdata(self, temp_dict):
        """
        validate user data for signup
        params: user information
        returns: bool or informative message
        """
        i=0
        print(temp_dict)
        for key,value in temp_dict.items():
            print(i) 
            if type(value)!=str:
                return jsonify({
                'message':'sorry! '+key+' field must be sequence of characters'
            }), 400
            
            if not value or value.isspace():
                print(i,'me')
                return jsonify({
                'message':'sorry! your '+key+' is required and can not be an empty string'
            }), 400
            
            if i < 2:
                user_dont_exist = self.check_user_dont_exist(key,value)
                if user_dont_exist != True:
                    return user_dont_exist
            i+=1
        return True


    def validate_user_login(self, data, admin=False):
        """
        Handle login
        params: user data
        returns: informative messsage
        """
        username = data.get('username')
        password = data.get('password')

        userdont_exist = self.check_user_dont_exist('username', username)

        if userdont_exist!=True:
            check_password = self.database.validate_password(username,password)
            return check_password
        return jsonify({'message':'Non existent user, please sign up'}), 400



    def check_user_dont_exist(self, key, value):
        """
        Check database for user existance
        """
        user_exists = self.database.check_availability_of_userdetails(key,value)
        
        if user_exists[0]['exists'] == True:
            return jsonify({
                'message':key+' is already taken'
            }), 400
        return True


    def validate_parcels_by_user(self, username, user_id):

        if len(Users.user_accounts==0):
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
    
    def validate_cancel_parcel_delivery_order(self, username,parcel_id):
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


    def validate_update_parcel_delivery_order(self, username, data, parcel_id):
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
    
    def validate_parcel_addition(self, username, data):
        """
        Validate parcel addition
        params: username, parcel information
        """
        parcel_description = data.get('parcel_description')
        recipient = data.get('recipient')
        contact = data.get('contact')
        pickup_location = data.get('pickup_location')
        destination =data.get('destination')
        status='pending'
        temp_parcel = dict(
            parcel_description=parcel_description,
            recipient=recipient,
            contact=contact,
            pickup_location=pickup_location,
            destination=destination
        )

        invalid_user = self.check_user_dont_exist('username',username)
        if invalid_user == True:
            return jsonify({
                'Message':'@'+username+' Lets make things official. Please signup'
            }), 400

        for key,value in temp_parcel.items():
            if type(value)!=str:
                return jsonify({
                    'message':'Your '+key+' should be a sequence of characters'
                }),400

            elif not value or value.isspace():
                return jsonify({
                    'message':'Please add your parcel'+key+'. It cannot be a space',
                }),400
        
        temp_parcel['username'] = username
        added_parcel = dict(self.database.add_parcel(temp_parcel))
        print(added_parcel)
        
        if type(added_parcel)==dict:
            return jsonify({
                'message' : 'hello! '+username+' Your Parcel Delivery order has been placed',
                'Parcel': added_parcel
            }),200
        
        return jsonify({
            'message' : '@'+username+' your parcel has not been added'
        })
    


    def validate_get_parcel_by_id(self, username,parcel_id):
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
    

    def validate_get_all_parcels(self, username):
        
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


    def validate_get_all_users(self,username):

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


    def weight_categories(self,username):
        """
        get available weight categories
        params:username
        returns: weight categories
        """
        sql_command = "SELECT * FROM weight_categories"
        self.database.insert_into_weight_categories()
        rows = self.database.execute_query(sql_command)
        return jsonify({
            '@'+username : 'Here are our available weight categories',
            'Categories' : rows
        })

