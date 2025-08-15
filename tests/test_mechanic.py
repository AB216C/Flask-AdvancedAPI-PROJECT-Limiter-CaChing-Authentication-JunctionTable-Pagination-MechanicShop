# from app import create_app
# from app.models import db

# import unittest

# class TestMechanic(unittest.TestCase):
#     def setUp(self):
#         self.app = create_app('TestingConfig')
#         with self.app.app_context():
#             db.drop_all()
#             db.create_all()
#         self.client = self.app.test_client()

#     def test_Create_mechanic(self):
#         mechanic_payload = {
#             "name": "John Peter",
#             "email": "johnp@gmail.com",
#             "phone": "345-234-5432",
#             "salary": "65,000"
#         }

#         response = self.client.post('/mechanics',json=mechanic_payload)
#         self.assertEqual(response.status_code,201)
#         self.assertEqual(response.json['name'], "John Peter")

#     def test_invalid_creation(self):
#         mechanic_payload = {
#             "name": "Jean Bosco",
#             "email": "jb@gmail.com",
#             "phone": "07834303939393",          
#         }

#         response = self.client.post('/mechanics',json=mechanic_payload)
#         self.assertEqual(response.status_code,404)
#         self.assertEqual(response.json['salary'],['Missing data for the required field']) 

#     def test_get_all_mechanic(self):
#         mechanic1 = {
#             "name": "John Jean",
#             "email": "jj@gmail.com",
#             "phone": "355-234-5432",
#             "salary": "65,000"
#         }

#         mechanic2 = {
#             "name": "John Mugabo",
#             "email": "jm1@gmail.com",
#             "phone": "315-234-5432",
#             "salary": "55,000"
#         } 

#         mechanic3 = {
#             "name": "John Mugisha",
#             "email": "jm@gmail.com",
#             "phone": "345-334-5432",
#             "salary": "75,000"
#         }
        
#         self.client.post('/mechanics', json=mechanic1)
#         self.client.post('/mechanics', json=mechanic2)
#         self.client.post('/mechanics', json=mechanic3)

#         response = self.client.get('/mechanics')
#         self.assertEqual(response.status_code,200)
#         self.assertEqual(len(response.json),3)

#         names = [item['name'] for item in response.json]
#         self.assertIn("John Jean", names)
#         self.assertIn("John Mugabo", names)
#         self.assertIn("John Mugisha", names)

#     def test_get_specific_mechanic(self):
#         mechanic_payload = {
#             "name": "John Peter",
#             "email": "johnp@gmail.com",
#             "phone": "345-234-5432",
#             "salary": "65,000"
#         }

#         response = self.client.post('/mechanics', json=mechanic_payload)
#         self.assertEqual(response.status_code,201)

#         mechanic_id = response.json['id']
#         response = self.client.get(f'/mechanics/{mechanic_id}')
#         self.assertEqual(response.status_code,200)
#         self.assertEqual(response.json['name'], "John Peter")

#     def test_get_non_existent_mechanic(self):
#         response = self.client.get('/mechanics/100')
#         self.assertEqual(response.status_code,404)
#         self.assertEqual(response.json['Error'], 'mechanic record not found')

    
#     def test_update_mechanic(self):
#         #CREATING A NEW Mechanic ITEM FIRST
#         response =self.client.post('/mechanics', json={
#             "name": "John Mugabo George",
#             "email": "jm1@gmail.com",
#             "phone": "315-234-5432",
#             "salary": "55,000"
#         })

#         mechanic_id = response.json['id']
#         #UPDATING THE Mechanic ITEM NEXT
#         update_payload = {
#             "name": "John Mugabo George Bush",
#             "email": "jm1235@gmail.com",
#             "phone": "315-234-5432",
#             "salary": "55,000"
#         }

#         updated_response = self.client.put(f'/mechanics/{mechanic_id}',json=update_payload)
#         self.assertEqual(updated_response.status_code,200)
#         self.assertEqual(updated_response.json['name'], 'John Mugabo George Bush')
#         self.assertEqual(updated_response.json['email'], 'jm1235@gmail.com')

#     def test_update_non_existent_mechanic(self):
#         update_payload = {
#             "name": " Shyirangabo Bush",
#             "email": "sb@gmail.com",
#             "phone": "34-234-5432",
#         }

#         updated_response = self.client.put(f'/mechanics/43',json=update_payload)
#         self.assertEqual(updated_response.status_code,404)
#         self.assertEqual(updated_response.json['Error'], 'The mechanic not found')

#     def test_delete_mechanic(self):
#         #CREATING A NEW Mechanic ITEM FIRST
#         response =self.client.post('/mechanics', json={
#             "name": "John Mugabo George Bush",
#             "email": "jm1235@gmail.com",
#             "phone": "315-234-5432",
#             "salary": "55,000"
#         })

#         mechanic_id = response.json['id']

#         #Then DELETE THE Mechanic
#         delete_response = self.client.delete(f'/mechanics/{mechanic_id}')
#         self.assertEqual(delete_response.status_code,200)
#         self.assertIn("successfully deleted", delete_response.json["Message"])

#     def test_delete_non_existent_mechanic(self):
#         delete_response = self.client.delete(f'/mechanics/43')
#         self.assertEqual(delete_response.status_code,404)
#         self.assertEqual(delete_response.json['Error'], 'The mechanic not found') 



# ## ===========TESTING SORTING MECHANICS===============