"""
Handles all validation as well as manipulation
"""
import datetime
from json import dumps
from flask import jsonify
from Application.models.users import Users
from Application.models.parcels import Parcels
from .database import Database

class Validation():
    """
    All validation
    """
    dbname=''
    def __init__(self):
        self.database = Database(Validation.dbname)


    def validate_signup(self, data, admin=False):
        """
        Validate user details during signup
        params: user information(dict)
        returns: tuple (json, status code)
        """
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

        if valid_data!=True:
            return valid_data

        user = temp_user
        user['admin'] = admin

        self.database.add_user(user)
        return jsonify({
            'message': 'hello! '+user['username']+' Your Account has been created. Please login',
        }), 201



    def validate_userdata(self, temp_dict):
        """
        validate user data for signup
        params: user information
        returns: bool or informative message
        """
        i=0
    
        for key,value in temp_dict.items():

            if type(value)!=str:
                return jsonify({
                'message':'sorry! '+key+' field must be sequence of characters'
            }), 400
            
            if not value or value.isspace():

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
        """
        Validate get parcels by user
        params:username and id
        returns:
        """
        user_id1 = self.get_user_id(username)
        user_admin = self.is_admin(username)
        if not user_admin:            
            if not user_id1 or user_id1!=user_id:
                return jsonify({
                    'Message' : '@'+username+' You have no authorization.'
                }), 403
        return self.get_parcels_by_user_id(user_id)
    
    def get_parcels_by_user_id(self,user_id):
        """
        Get parcels by user id
        """
        sql_command="""
        SELECT * FROM parcels where user_id={user_id};
        """.format(user_id=user_id)
        rows = self.database.execute_query(sql_command)
        if not rows:
            return jsonify({
                'Message': 'no parcel delivery orders from specified user'
            }), 404
        rows = self.tostring_for_date_time(rows)

        return jsonify({
            'parcels by user' : rows
        }), 200

    
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
            }), 401

        for key,value in temp_parcel.items():
            if type(value)!=str:
                return jsonify({
                    'message':'Your '+key+' should be a sequence of characters'
                }), 400

            elif not value or value.isspace():
                return jsonify({
                    'message':'Please add your parcel'+key+'. It cannot be a space',
                }), 400
        
        temp_parcel['username'] = username
        added_parcel = dict(self.database.add_parcel(temp_parcel))

        
        if type(added_parcel)==dict:
            return jsonify({
                'message' : 'hello! '+username+' Your Parcel Delivery order has been placed',
                'Parcel': added_parcel
            }), 201
        
        return jsonify({
            'message' : '@'+username+' your parcel has not been added'
        }), 400
    


    def validate_get_parcel_by_id(self, username,parcel_id):
        """
        Get parcels by id
        params: username, parcel id
        return: parcel
        """
        user_is_admin = self.is_admin(username)
        print(user_is_admin)
        if not user_is_admin:
            return jsonify({
                'Message': ' you do not have authorization'
            }), 400

        exists = self.check_if_parcel_id_exists(parcel_id)
        if exists!=True:
            return exists
        
        sql_command = """
        SELECT * FROM parcels where parcel_id={};
        """.format(parcel_id)
        rows = self.database.execute_query(sql_command)
        
        rows = self.tostring_for_date_time(rows)

        return jsonify({
            'Parcel' : rows
        }), 200
    

    def validate_get_all_parcels(self, username):
        """
        get all parcels
        """
        return self.get_all(username,'parcels')

    
    def get_user_id(self,username):
        """
        Get user id
        """
        user_id = self.database.get_from_users('user_id', username)
        if not user_id:
            return jsonify({
                'Message' : '@'+username+' lets make things official. Sign up with send it'
            }), 401
        return user_id

    def validate_get_all_users(self,username):
        """
        Get all users
        """
        return self.get_all(username,'users')

    def get_all(self, username, table):
        is_user_admin = self.is_admin(username)
        if not is_user_admin:
            return jsonify({
                'Message': '@'+username+', you are not authorized to view this.'
            }), 403
        sql_command="""
        SELECT * FROM {};
        """.format(table)
        all_elements = self.database.execute_query(sql_command)
        if not all_elements:
            return jsonify({
                'Users':'No '+table+' in system'
            }), 404
        all_elements = self.tostring_for_date_time(all_elements)
        return jsonify({
            'All '+table+'': all_elements
            }), 200


    def tostring_for_date_time(self, parcels):
        """
        Convert datetime to string for easy jsonification
        """
        for element in parcels:
            for key,value in element.items():
                if key == 'date_created' or key == 'date_to_be_delivered':
                    value == str(value)
        return parcels


    def check_if_parcel_id_exists(self,parcel_id):
        id_exists = self.database.parcel_exists(parcel_id)
        if id_exists == False:
            return jsonify({
                'message' : 'Invalid parcel'
            }), 404

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
        categories = str(rows.copy())
        return jsonify({
            '@'+username : 'Here are our available weight categories',
            'Categories' : categories
        }), 200


    def validate_change_present_location(self, username, parcel_id ,data):
        """
        Change the present location location of parcel
        """
        return self.update_parcel_by_admin(username, parcel_id, data, 'current_location')


    def update_parcel_by_admin(self, username, parcel_id, data, column):
        """
        Update parcel by admin only
        """
        if self.is_admin(username)!=True:
            return jsonify({
                'message':'@'+username+' You are not authorized to do this'
            }), 403
        column_data = data.get(column)
        if not column_data or column_data.isspace():
            return jsonify({
                'Message': column+' should be a sequence of characters'
            }), 400
        
        exists = self.check_if_parcel_id_exists(parcel_id)
        if exists != True:
            return exists
        
        updated_fields = self.database.change_status(column, column_data, parcel_id)
        if not updated_fields:
            return jsonify({
                'Message' : 'Update '+column+' failed'
            }), 400
        
        return jsonify({
            'Message' : 'Update successful',
            'Updated fields' : updated_fields
        }), 200


    def validate_change_status(self, username, parcel_id, data):
        """
        Change the status of the parcel delivery order
        """
        status = data.get('status')
        if status == 'pending' or status == 'in transit' or status == 'canceled' or status == 'delivered':
            return self.update_parcel_by_admin(username, parcel_id, data, 'status')
        return jsonify({
            'Message' : 'Status has to be pending, or in transit, or canceled, or delivered'
        }), 400


    def validate_change_destination(self,username,parcel_id, data):
        """
        Change the destination of the parcel delivery order
        """
        destination = data.get('destination')
        if not destination or destination.isspace():
            return jsonify({
                'Messsage' : 'Destination has to be a sequence of characters and cannot be a blank space'
        }), 400
        user_id = self.get_user_id(username)
        if type(user_id)==tuple:
            return user_id
        if self.check_user_created_parcel(user_id, parcel_id)!=True:
            return jsonify({
                'message' : 'You did not create the parcel'
            }), 403
            
        updated_fields = self.database.change_status('destination', destination, parcel_id)
        if not updated_fields:
            return jsonify({
            'Message' : 'Update destination failed'
            }), 400
    
        return jsonify({
            'message' : 'Updated destination',
            'updated fields' : updated_fields
        }), 200




    def is_admin(self,username):
        """
        Check if user is admin
        params: n/a
        returns:n/a
        """
        is_admin = self.database.get_from_users('admin', username)
        return is_admin


    def check_user_created_parcel(self, user_id, parcel_id):
        """
        Check if user created parcel
        """
        sql_command = """
        SELECT EXISTS(SELECT * FROM parcels where parcel_id={parcel_id} and user_id={user_id})
        """.format(parcel_id=parcel_id,user_id=user_id)
        rows = self.database.execute_query(sql_command)
        return rows[0]['exists']
