# from app import create_app
# from app.models import db

# import unittest

# class TestCustomer(unittest.TestCase):
#     def setUp(self):
#         self.app = create_app('TestingConfig')
#         with self.app.app_context():
#             db.drop_all()
#             db.create_all()
#         self.client = self.app.test_client()

#     def test_Create_customer(self):
#         customer_payload = {
#             "name": "Jean Bosco",
#             "email": "jb@gmail.com",
#             "phone": "07834303939393",
#             "password": "jb2025"
#         }

#         response = self.client.post('/customers',json=customer_payload)
#         self.assertEqual(response.status_code,201)
#         self.assertEqual(response.json['name'], "Jean Bosco")

#     def test_invalid_creation(self):
#         customer_payload = {
#             "name": "Jean Bosco",
#             "email": "jb@gmail.com",
#             "phone": "07834303939393",          
#         }

#         response = self.client.post('/customers',json=customer_payload)
#         self.assertEqual(response.status_code,400)
#         self.assertEqual(response.json['password'],['Missing data for the required field'])  

#     def test_get_specific_customer(self):
#         customer_payload = {
#             "name": "John Peter",
#             "email": "johnp@gmail.com",
#             "phone": "345-234-5432",
#             "password": "65,000password"
#         }

#         response = self.client.post('/customers', json=customer_payload)
#         self.assertEqual(response.status_code,201)

#         customer_id = response.json['id']
#         response = self.client.get(f'/customers/{customer_id}')
#         self.assertEqual(response.status_code,200)
#         self.assertEqual(response.json['name'], "John Peter")

#     def test_get_non_existent_customer(self):
#         response = self.client.get('/customers/100')
#         self.assertEqual(response.status_code,404)
#         self.assertEqual(response.json['Error'], 'customer record not found')   


