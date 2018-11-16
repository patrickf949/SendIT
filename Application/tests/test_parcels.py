import unittest
import json
import pytest
from Application import app,create_app
from Application.views import *
from .testdata import TestData

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

    
    
    def test_admin_signup_valid_params(self):
        
        response = self.test_client.post(
            '/api/v1/admin/signup',
            content_type='application/json',
            data=json.dumps(self.testdata.valid_admin_signup)
        )
        self.assertEqual(response.status_code, 200)
    
    def test_admin_signup_invalid_params(self):
        
        response = self.test_client.post(
            '/api/v1/admin/signup',
            content_type='application/json',
            data=json.dumps(self.testdata.invalid_admin_signup)
        )
        self.assertEqual(response.status_code, 400)
    

    def test_admin_signup_empty(self):
        response = self.test_client.post(
            '/api/v1/admin/signup',
            content_type='application/json',
            data=json.dumps(self.testdata.empty)
        )
        self.assertEqual(response.status_code, 400)


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
        self.testdata.add_parcel_delivery_order()
        response = self.test_client.put(
            '/api/v1/parcels/1/update',
            content_type='application/json',
            data=json.dumps(self.testdata.valid_parcel)
        )
        self.assertEqual(response.status_code,200)

    def test_parcel_update_lessparams(self):
        self.testdata.add_parcel_delivery_order()
        response = self.test_client.put(
            '/api/v1/parcels/1/update',
            content_type='application/json',
            data=json.dumps(self.testdata.invalid_parcel_less_params)
        )
        self.assertEqual(response.status_code,400)


    def test_parcel_update_passuserdetails(self):
        self.testdata.add_parcel_delivery_order()
        response = self.test_client.put(
            '/api/v1/parcels/1/update',
            content_type='application/json',
            data=json.dumps(self.testdata.valid_admin_login)
        )
        self.assertEqual(response.status_code,400)

    

    def tearDown(self):
        return super().tearDown()

    