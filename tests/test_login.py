from app import create_app
from app.models import db,Customer
from datetime import datetime 
from app.utils.util import encode_token
import unittest

class TestCustomerLogin(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.customer = Customer(name="Peter Buntu", email= "pbuntu@gmail.com", phone="1234567", password="password123")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
        self.token = encode_token(1)       #customer id is 1
        self.client = self.app.test_client()

    def test_login_customer(self):
        credentials = {
            "email": "pbuntu@gmail.com",
            "password": "password123"
        }

        response = self.client.post('/customer/login', json=credentials)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json['status'], 'success')
        return response.json['token']
    
    def test_invalid_login(self):
        credentials = {
            "email": "wrongpbuntu@gmail.com",
            "password": "wrongpassword"
        }

        response = self.client.post('/customer/login', json=credentials)
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json['message'], 'invalid email or password')

    

