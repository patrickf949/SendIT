import unittest
from flask import Response,request
import json
import pytest
from Application import create_app
from Application.views import *
from .testdata import TestData
from Application.config import app_config
from Application.controllers.database import Database

class TestSendIT(unittest.TestCase):
    """
    This class tests our api endpoints
    """
    def setUp(self):
        self.env = app_config['testing']
        self.app = create_app(self.env)
        self.test_client = self.app.test_client()
  
        Database.dbname = self.env.dbname
        self.testdata = TestData()
        self.table_drop = Database(self.env.dbname)
        self.usertoken=''
        self.admintoken=''
    
    
    def test_istestdata_instance(self):
        assert isinstance(self.testdata, TestData)


    def change_session(self, token):
        """
        Set the authorization header
        """
        request.headers.set('Authorisation',f'Bearer {token}')
        

    def auser_signup(self, email, password):
        response = self.test_client.post(
            'api/v2/auth/signup',
            data=json.dumps(self.testdata.valid_admin_signup),
        content_type='application/json')
        message = response.get_json()
        self.assertEqual(message.status_code,200)
        
    
    def test_get_all_parcels(self):
        response = self.test_client.get(
            '/api/v2/parcels',
            content_type='application/json',
        )
        message = response.get_json()
        self.assertEqual(response.status_code,401)
    
    def test_get_all_parcels_when_empty(self):

        response = self.test_client.get(
            '/api/v2/parcels',
            content_type='application/json',
        )
        message = response.get_json()
        self.assertEqual(message.get('msg'),'Missing Authorization Header' )
        self.assertEqual(response.status_code,401)

    
    def test_signup_invalid_params(self):
        
        response = self.test_client.post(
            '/api/v2/auth/signup',
            content_type='application/json',
            data=json.dumps(self.testdata.invalid_admin_signup)
        )
        message = response.get_json()
        self.assertEqual(response.status_code, 400)


    def test_adminlogin_valid_params(self):
        
        response = self.test_client.post(
            '/api/v2/auth/login',
            content_type='application/json',
            data=json.dumps(self.testdata.valid_admin_login)
        )
        message = response.get_json()
        self.admintoken = message.get('Access_token')
        self.assertEqual(response.status_code, 200)

    def test_adminlogin_invalid_params(self):
        response = self.test_client.post(
            '/api/v2/auth/login',
            content_type='application/json',
            data=json.dumps(self.testdata.invalid_admin_login)
        )

        self.assertEqual(response.status_code, 400)

    def test_user_signup_valid_params(self):
        
        response = self.test_client.post(
            '/api/v2/auth/signup',
            content_type='application/json',
            data=json.dumps(self.testdata.valid_user_signup)
        )
        
        self.assertEqual(response.status_code, 200)
    
    def test_user_signup_invalid_params(self):

        response = self.test_client.post(
            '/api/v2/auth/signup',
            content_type='application/json',
            data=json.dumps(self.testdata.invalid_admin_signup)
        )
        self.assertEqual(response.status_code, 400)
    

    def test_user_signup_empty(self):
        response = self.test_client.post(
            '/api/v2/auth/signup',
            content_type='application/json',
            data=json.dumps(self.testdata.empty)
        )
        self.assertEqual(response.status_code, 400)


    def test_auser_login(self):
        
        response = self.test_client.post(
            '/api/v2/auth/login',
            content_type='application/json',
            data=json.dumps(self.testdata.valid_user_login)
        )
        message = response.get_json()
        print(message)
        self.usertoken = message['Access_token']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(message.get('message'), 'Hello TestUser you are logged into SendIT')
        
        

    def test_valid_parcel_addition(self):
        # self.change_session(self.usertoken)
        response = self.test_client.post(
            '/api/v2/parcels',
            content_type='application/json',
            data=json.dumps(self.testdata.valid_parcel)
        )
        
        message = response.get_json()
        self.assertEqual(message.get('msg'),'Missing Authorization Header')

        self.assertEqual(response.status_code,401)

    
    def test_invalid_parcel_addition(self):
        response = self.test_client.post(
            '/api/v2/parcels',
            content_type='application/json',
            data=json.dumps(self.testdata.invalid_parcel_less_params)
        )
        # message = response.get_json()
        self.assertEqual(response.status_code, 401)


    def test_parcel_addition_invalid_recipient(self):
        response = self.test_client.post(
            '/api/v2/parcels',
            content_type='application/json',
            data=json.dumps(self.testdata.invalid_recipient_parcel)
        )
        self.assertEqual(response.status_code, 401)
    
    
    
    def test_parcel_addition_invalid_contact(self):
        response = self.test_client.post(
            '/api/v2/parcels',
            content_type='application/json',
            data=json.dumps(self.testdata.invalid_recipient_parcel)
        )
        self.assertEqual(response.status_code,401)
    

    def test_parcel_addition_lessparams(self):

        response = self.test_client.post(
            '/api/v2/parcels',
            content_type='application/json',
            data=json.dumps(self.testdata.invalid_parcel_less_params)
        )
        self.assertEqual(response.status_code,401)
    
    
    def test_parcel_addition_empty(self):
        
        response = self.test_client.post(
            '/api/v2/parcels',
            content_type='application/json',
            data=json.dumps(self.testdata.empty)
        )
        self.assertEqual(response.status_code,401)

    def test_parcel_update_empty(self):
        response = self.test_client.put(
            '/api/v2/parcels/1/destination',
            content_type='application/json',
            data=json.dumps(self.testdata.empty)
        )
        self.assertEqual(response.status_code,401)
    
    def test_parcel_update_valid(self):
        response = self.test_client.put(
            '/api/v2/parcels/1/destination',
            content_type='application/json',
            data=json.dumps(self.testdata.valid_parcel)
        )
        self.assertEqual(response.status_code,401)

    def test_parcel_update_lessparams(self):
        response = self.test_client.put(
            '/api/v2/parcels/1/destination',
            content_type='application/json',
            data=json.dumps(self.testdata.invalid_parcel_less_params)
        )
        self.assertEqual(response.status_code,401)


    def test_parcel_update_passuserdetails(self):

        response = self.test_client.put(
            '/api/v2/parcels/1/status',
            content_type='application/json',
            data=json.dumps(self.testdata.valid_admin_login)
        )
        self.assertEqual(response.status_code,401)
    
    def test_parcel_update_presentlocation(self):

        response = self.test_client.put(
            '/api/v2/parcels/1/presentLocation',
            content_type='application/json',
            data=json.dumps(self.testdata.valid_admin_login)
        )
        self.assertEqual(response.status_code,401)

    @pytest.mark.skip(reason="no way of currently testing this")
    def test_cancel_parcel_delivery_order(self):
        
        response = self.test_client.get(
            '/api/v2/parcels/1/cancel',
            content_type='application/json',
        )
        self.assertEqual(response.status_code,401)

    @pytest.mark.skip(reason="no way of currently testing this")
    def test_cancel_invalid_parcel_delivery_ordedr(self):
        
        response = self.test_client.get(
            '/api/v2/parcels/43/cancel',
            content_type='application/json',
        )
        self.assertEqual(response.status_code,401)
    

    def test_get_valid_parcel_by_id(self):
        
        
        response = self.test_client.get(
            '/api/v2/parcels/3',
            content_type='application/json'
        )
        self.assertEqual(response.status_code,401)


    def test_get_invalid_parcel_by_id(self):

        response = self.test_client.get(
            '/api/v2/parcels/43',
            content_type='application/json'
        )
        self.assertEqual(response.status_code,401)


    def test_get_parcels_by_user_id(self):
 
        response = self.test_client.get(
            '/api/v2/parcels/43',
            content_type='application/json'
        )
        self.assertEqual(response.status_code,401)

    def test_get_all_users(self):

        response = self.test_client.get(
            '/api/v2/users',
            content_type='application/json'
        )
        message = response.get_json()
        self.assertEqual(message.get('msg'),'Missing Authorization Header')
        self.assertEqual(response.status_code,401)


    def tearDown(self):
        self.table_drop.drop_all_tables()
