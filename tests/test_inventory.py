# from app import create_app
# from app.models import db

# import unittest

# class TestInventory(unittest.TestCase):
#     def setUp(self):
#         self.app = create_app('TestingConfig')
#         with self.app.app_context():
#             db.drop_all()
#             db.create_all()
#         self.client = self.app.test_client()

#     def test_Create_inventory(self):
#         inventory_payload = {
#             "part_name": "control arm",
#             "part_number": "3453",
#             "price": 454.50,

#         }

#         response = self.client.post('/inventory',json=inventory_payload)
#         self.assertEqual(response.status_code,201)
#         self.assertEqual(response.json['part_name'], "control arm")

#     def test_invalid_creation(self):
#         inventory_payload = {
#             "part_name": "Engine oil",
#             "part_number": "34533",         
#         }

#         response = self.client.post('/inventory',json=inventory_payload)
#         self.assertEqual(response.status_code,400)
#         self.assertEqual(response.json['price'],['Missing data for the required field'])

#     def test_get_all_inventory(self):
#         item1 = {
#             "part_name": "Brake pads",
#             "part_number": "1234",
#             "price": 150.00
#         }

#         item2 = {
#             "part_name": "Spark plugs",
#             "part_number": "5678",
#             "price": 75.00
#         }

#         self.client.post('/inventory', json=item1)
#         self.client.post('/inventory', json=item2)

#         response = self.client.get('/inventory')
#         self.assertEqual(response.status_code,200)
#         self.assertEqual(len(response.json),2)

#         part_names = [item['part_name'] for item in response.json]
#         self.assertIn("Brake pads", part_names)
#         self.assertIn("Spark plugs", part_names)

#     def test_get_specific_inventory(self):
#         inventory_payload = {
#             "part_name": "control arm",
#             "part_number": "3453",
#             "price": 454.50
#         }

#         response = self.client.post('/inventory', json=inventory_payload)
#         self.assertEqual(response.status_code,201)

#         inventory_id = response.json['id']
#         response = self.client.get(f'/inventory/{inventory_id}')
#         self.assertEqual(response.status_code,200)
#         self.assertEqual(response.json['part_name'], "control arm")

#     def test_get_non_existent_inventory(self):
#         response = self.client.get('/inventory/100')
#         self.assertEqual(response.status_code,404)
#         self.assertEqual(response.json['Error'], 'Inventory record not found')

    
#     def test_update_inventory(self):
#         #CREATING A NEW INVENTORY ITEM FIRST
#         response =self.client.post('/inventory', json={
#             "part_name": "Radiator",
#             "part_number": "9000",
#             "price": 450.04
#         })

#         inventory_id = response.json['id']
#         #UPDATING THE INVENTORY ITEM NEXT
#         update_payload = {
#             "part_name": "Radiator 250",
#             "part_number": "8900",
#             "price": 450.04
#         }

#         updated_response = self.client.put(f'/inventory/{inventory_id}',json=update_payload)
#         self.assertEqual(updated_response.status_code,200)
#         self.assertEqual(updated_response.json['part_name'], 'Radiator 250')
#         self.assertEqual(updated_response.json['part_number'], '8900')

#     def test_update_non_existent_inventory(self):
#         update_payload = {
#             "part_name": "Rad",
#             "part_number": "80",
#         }

#         updated_response = self.client.put(f'/inventory/43',json=update_payload)
#         self.assertEqual(updated_response.status_code,404)
#         self.assertEqual(updated_response.json['Error'], 'The inventory not found')

#     def test_delete_inventory(self):
#         #CREATING A NEW INVENTORY ITEM FIRST
#         response =self.client.post('/inventory', json={
#             "part_name": "oil filter",
#             "part_number": "3000",
#             "price": 450.04
#         })

#         inventory_id = response.json['id']

#         #Then DELETE THE INVENTORY
#         delete_response = self.client.delete(f'/inventory/{inventory_id}')
#         self.assertEqual(delete_response.status_code,200)
#         self.assertIn("successfully deleted", delete_response.json["Message"])

#     def test_delete_non_existent_inventory(self):
#         delete_response = self.client.delete(f'/inventory/43')
#         self.assertEqual(delete_response.status_code,404)
#         self.assertEqual(delete_response.json['Error'], 'The inventory not found')












