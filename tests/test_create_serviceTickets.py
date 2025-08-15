# from app import create_app
# from app.models import db,Customer

# import unittest

# class TestServiceTicket(unittest.TestCase):
#     def setUp(self):
#         self.app = create_app('TestingConfig')
#         with self.app.app_context():
#             db.drop_all()
#             db.create_all()
#         self.client = self.app.test_client()

#     def test_Create_service_ticket(self):
#         service_ticket_payload = {
#             "VIN": "34555-zzzz-y",
#             "service_date": "2000-03-23",
#             "customer_id": 1
#         }

#         response = self.client.post('/service_tickets',json=service_ticket_payload)
#         self.assertEqual(response.status_code,201)
#         self.assertEqual(response.json['VIN'], "34555-zzzz-y")

#     def test_invalid_creation(self):
#         service_ticket_payload = {
#             "VIN": "34555-zzzz-yuuux",
#             "service_date": "2000-03-25",
#         }

#         response = self.client.post('/service_tickets',json=service_ticket_payload)
#         self.assertEqual(response.status_code,400)
#         self.assertEqual(response.json['customer_id'],['Missing data for the required field'])    