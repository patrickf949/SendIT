import unittest
import json
import pytest
from Application import app,create_app
from Application.views import *
from .testdata import TestData
from Application.models.parcels import Parcels
from Application.models.users import Users

class TestSendIT(unittest.TestCase):
    """
    This class tests our api endpoints
    """
    def setUp(self):
        self.app = create_app()
        self.test_client = self.app.test_client()
        self.testdata = TestData()
    
    
    def test_istestdata_instance(self):
        assert isinstance(self.testdata, TestData)

    
    def test_get_all_parcels(self):    
        self.testdata.add_parcel_delivery_order(TestData.valid_parcel)
        response = self.test_client.get(
            '/api/v1/parcels',
            content_type='application/json',
        )
        message = json.loads(response.data.decode())

        self.assertEqual(response.status_code,200)
        self.assertEqual(message['parcels'], Parcels.parcels)
    
    def test_get_all_parcels_when_empty(self):
        self.testdata.empty_all_lists()
        response = self.test_client.get(
            '/api/v1/parcels',
            content_type='application/json',
        )
        message = json.loads(response.data.decode())
        self.assertEqual(message['message'],'No parcels added yet' )
        self.assertEqual(response.status_code,400)


    
    def test_admin_signup_valid_params(self):
        
        response = self.test_client.post(
            '/api/v1/admin/signup',
            content_type='application/json',
            data=json.dumps(self.testdata.valid_admin_signup)
        )
        message = json.loads(response.data.decode())

        self.assertEqual(message['message'],'hello! Andrew You Account has been created and automatically logged in')
        self.assertEqual(response.status_code, 200)
    
    
    def test_admin_signup_invalid_params(self):
        
        response = self.test_client.post(
            '/api/v1/admin/signup',
            content_type='application/json',
            data=json.dumps(self.testdata.invalid_admin_signup)
        )
        message = json.loads(response.data.decode())
        self.assertEqual(message['message'], 'sorry! All fields must be strings')
        self.assertEqual(response.status_code, 400)
    

    def test_admin_signup_empty(self):
        response = self.test_client.post(
            '/api/v1/admin/signup',
            content_type='application/json',
            data=json.dumps(self.testdata.empty)
        )
        self.temp_parcels = Parcels.parcels
        message = json.loads(response.data.decode())
        self.assertEqual(message['message'], 'sorry! All fields must be strings')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Parcels.parcels,self.temp_parcels)
        


    @pytest.mark.skip(reason="no way of currently testing this")
    def test_admin_login_valid_params(self):
        
        response = self.test_client.post(
            '/api/v1/admin/login',
            content_type='application/json',
            data=json.dumps(self.testdata.valid_admin_login)
        )
        
        self.assertEqual(response.status_code, 200)

    def test_user_signup_valid_params(self):
        
        response = self.test_client.post(
            '/api/v1/signup',
            content_type='application/json',
            data=json.dumps(self.testdata.valid_user_signup)
        )
        self.assertEqual(response.status_code, 200)
    
    def test_user_signup_invalid_params(self):
        
        response = self.test_client.post(
            '/api/v1/signup',
            content_type='application/json',
            data=json.dumps(self.testdata.invalid_admin_signup)
        )
        self.assertEqual(response.status_code, 400)
    

    def test_user_signup_empty(self):
        response = self.test_client.post(
            '/api/v1/admin/signup',
            content_type='application/json',
            data=json.dumps(self.testdata.empty)
        )
        self.assertEqual(response.status_code, 400)


    @pytest.mark.skip(reason="no way of currently testing this")
    def test_user_login(self):
        
        response = self.test_client.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(self.testdata.valid_user_login)
        )
        
        self.assertEqual(response.status_code, 200)

    def test_valid_parcel_addition(self):
        response = self.test_client.post(
            '/api/v1/parcels',
            content_type='application/json',
            data=json.dumps(self.testdata.valid_parcel)
        )
        
        self.assertEqual(response.status_code,200)

    
    def test_invalid_parcel_addition(self):
        response = self.test_client.post(
            '/api/v1/parcels',
            content_type='application/json',
            data=json.dumps(self.testdata.invalid_parcel_less_params)
        )
        # message = json.loads(response.status_code())
        self.assertEqual(response.status_code, 400)
    
    
    
    def test_parcel_addition_invalid_recipient(self):
        response = self.test_client.post(
            '/api/v1/parcels',
            content_type='application/json',
            data=json.dumps(self.testdata.invalid_recipient_parcel)
        )
        self.assertEqual(response.status_code, 400)
    
    
    
    def test_parcel_addition_invalid_contact(self):
        response = self.test_client.post(
            '/api/v1/parcels',
            content_type='application/json',
            data=json.dumps(self.testdata.invalid_recipient_parcel)
        )
        self.assertEqual(response.status_code,400)
    

    def test_parcel_addition_lessparams(self):

        response = self.test_client.post(
            '/api/v1/parcels',
            content_type='application/json',
            data=json.dumps(self.testdata.invalid_parcel_less_params)
        )
        self.assertEqual(response.status_code,400)
    
    
    def test_parcel_addition_empty(self):
        
        response = self.test_client.post(
            '/api/v1/parcels',
            content_type='application/json',
            data=json.dumps(self.testdata.empty)
        )
        self.assertEqual(response.status_code,400)

    def test_parcel_update_empty(self):
        response = self.test_client.put(
            '/api/v1/parcels/1/update',
            content_type='application/json',
            data=json.dumps(self.testdata.empty)
        )
        self.assertEqual(response.status_code,400)
    
    def test_parcel_update_valid(self):
        self.testdata.add_parcel_delivery_order(TestData.valid_parcel)
        response = self.test_client.put(
            '/api/v1/parcels/1/update',
            content_type='application/json',
            data=json.dumps(self.testdata.valid_parcel)
        )
        self.assertEqual(response.status_code,200)

    def test_parcel_update_lessparams(self):
        self.testdata.add_parcel_delivery_order(TestData.valid_parcel)
        response = self.test_client.put(
            '/api/v1/parcels/1/update',
            content_type='application/json',
            data=json.dumps(self.testdata.invalid_parcel_less_params)
        )
        self.assertEqual(response.status_code,400)


    def test_parcel_update_passuserdetails(self):
        self.testdata.add_parcel_delivery_order(TestData.valid_parcel)
        response = self.test_client.put(
            '/api/v1/parcels/1/update',
            content_type='application/json',
            data=json.dumps(self.testdata.valid_admin_login)
        )
        self.assertEqual(response.status_code,400)

    def test_cancel_parcel_delivery_order(self):
        self.testdata.add_parcel_delivery_order(TestData.valid_parcel)
        response = self.test_client.get(
            '/api/v1/parcels/1/cancel',
            content_type='application/json',
        )
        self.assertEqual(response.status_code,200)

    def test_cancel_invalid_parcel_delivery_ordedr(self):
        self.testdata.add_parcel_delivery_order(TestData.valid_parcel)
        response = self.test_client.get(
            '/api/v1/parcels/43/cancel',
            content_type='application/json',
        )
        self.assertEqual(response.status_code,400)
    

    def test_get_valid_parcel_by_id(self):
        
        self.testdata.add_parcel_delivery_order(TestData.valid_parcel)
        response = self.test_client.get(
            '/api/v1/parcels/3',
            content_type='application/json'
        )
        self.assertEqual(response.status_code,200)


    def test_get_invalid_parcel_by_id(self):
        self.testdata.add_parcel_delivery_order(TestData.valid_parcel)
        response = self.test_client.get(
            '/api/v1/parcels/43',
            content_type='application/json'
        )
        self.assertEqual(response.status_code,400)
    

    def test_get_parcels_by_user_id(self):
        self.testdata.add_parcel_delivery_order(TestData.valid_parcel)
        self.testdata.add_parcel_delivery_order(TestData.valid_parcel1)
        
        response = self.test_client.get(
            '/api/v1/parcels/43',
            content_type='application/json'
        )
        self.assertEqual(response.status_code,400)
    
    def test_get_all_users(self):
        self.testdata.empty_all_lists()
        response = self.test_client.get(
            '/api/v1/users',
            content_type='application/json'
        )
        self.assertEqual(response.status_code,400)
        
        

    def tearDown(self):
        return super().tearDown()

    