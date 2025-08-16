from app import create_app
from app.models import db,Customer, Service_ticket,Mechanic, Inventory
from datetime import date

import unittest

class TestServiceTicket(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.app.test_client()

    def test_Create_service_ticket(self):
        service_ticket_payload = {
            "VIN": "34555-zzzz-y",
            "service_date": "2000-03-23",
            "customer_id": 1
        }

        response = self.client.post('/service_tickets',json=service_ticket_payload)
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.json['VIN'], "34555-zzzz-y")

    def test_invalid_creation(self):
        service_ticket_payload = {
            "VIN": "34555-zzzz-yuuux",
            "service_date": "2000-03-25",
        }

        response = self.client.post('/service_tickets',json=service_ticket_payload)
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json['customer_id'],['Missing data for required field.'])


    def test_all_service_tickets(self):
        with self.app.app_context():

            customer = Customer(name="Jean Bosco",
                                email="jb@gmail.com",
                                phone="07834303939393",
                                password="jb2025")

            db.session.add(customer)
            db.session.commit()
            
            ticket = Service_ticket(
                VIN = "34433-VVV-343",
                service_date = date(2000,2,13),
                customer_id = customer.id
            )
            db.session.add(ticket)
            db.session.commit()

        response = self.client.get('/service_tickets')
        self.assertEqual(response.status_code,200)
        self.assertIsInstance(response.json,list)
        self.assertGreaterEqual(len(response.json),1)

    def test_retrive_specific_service_tickets(self):
        with self.app.app_context():

            customer = Customer(name="Jean Bosco",
                                email="jb@gmail.com",
                                phone="07834303939393",
                                password="jb2025")

            db.session.add(customer)
            db.session.commit()
            
            service_ticket = Service_ticket(
                VIN = "34433-VVV-343",
                service_date = date(2000,2,13),
                customer_id = customer.id
            )
            db.session.add(service_ticket)
            db.session.commit()

            service_ticket_id = service_ticket.id

        response = self.client.get(f'/service_tickets/{service_ticket_id}')
        self.assertEqual(response.status_code,200)
        self.assertIsInstance(response.json,dict)
        self.assertEqual(response.json['VIN'],"34433-VVV-343")


    def test_delete_specific_service_tickets(self):
        with self.app.app_context():

            customer = Customer(name="Jean Bosco",
                                email="jb@gmail.com",
                                phone="07834303939393",
                                password="jb2025")

            db.session.add(customer)
            db.session.commit()
            
            service_ticket = Service_ticket(
                VIN = "34433-VVV-343",
                service_date = date(2000,2,13),
                customer_id = customer.id
            )
            db.session.add(service_ticket)
            db.session.commit()

            service_ticket_id = service_ticket.id

        response = self.client.delete(f'/service_tickets/{service_ticket_id}')
        self.assertEqual(response.status_code,200)
        self.assertIn("successfully deleted", response.json['Message'])


    def test_edit_specific_service_ticket(self):
        with self.app.app_context():

            customer = Customer(name="Jean Bosco",
                                email="jb@gmail.com",
                                phone="07834303939393",
                                password="jb2025")

            db.session.add(customer)
            db.session.commit()

            mechanic1 = Mechanic(name="Shimwa Bosco",
                                email="sb@gmail.com",
                                phone="0783430393444",
                                salary="65,000")
            
            mechanic2 = Mechanic(name="Shimwa Peter",
                    email="sp@gmail.com",
                    phone="07834303939",
                    salary="55,000")
            db.session.add_all([mechanic1,mechanic2])
            db.session.commit()

            
            service_ticket = Service_ticket(
                VIN = "34433-VVV-343",
                service_date = date(2000,2,13),
                customer_id = customer.id
            )

            service_ticket.mechanics.append(mechanic2)
            db.session.add(service_ticket)
            db.session.commit()

            payload = {
                "add_mechanic_ids": [mechanic1.id],
                "remove_mechanic_ids": [mechanic2.id]
            }

            service_ticket_id = service_ticket.id



        response = self.client.put(f'/service_tickets/{service_ticket_id}', json = payload)
        self.assertEqual(response.status_code,200)
        self.assertIn(mechanic1.id, [mechanic['id'] for mechanic in response.json['mechanics']])
        self.assertNotIn(mechanic2.id, [mechanic['id'] for mechanic in response.json['mechanics']])


    def test_add_inventory_to_service_ticket(self):
        with self.app.app_context():

            customer = Customer(name="Jean Bosco",
                                email="jb@gmail.com",
                                phone="07834303939393",
                                password="jb2025")

            db.session.add(customer)
            db.session.commit()

            
            service_ticket = Service_ticket(
                VIN = "34433-VVV-343",
                service_date = date(2000,2,13),
                customer_id = customer.id
            )

            db.session.add(service_ticket)

            inventory= Inventory(part_name="oil filter", part_number="OF-123", price=455.40)
            db.session.add(inventory)
            db.session.commit()

            payload = {
                "part_id": inventory.id,
                "quantity": 2
            }

            service_ticket_id = service_ticket.id



        response = self.client.post(f'/service_tickets/{service_ticket_id}/add_inventory', json = payload)
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.json["quantity"],2)
        self.assertEqual(response.json["part_id"],inventory.id)



    def test_add_mechanic_to_service_ticket(self):
        with self.app.app_context():

            customer = Customer(name="Jeanne Marie",
                                email="jm@gmail.com",
                                phone="07834303939393",
                                password="jm2025")

            db.session.add(customer)

            mechanic = Mechanic(name="Shimwa Jean Bosco",
                                email="sj@gmail.com",
                                phone="0783430393444",
                                salary="66,000")
            
            db.session.add(mechanic)
            db.session.commit()

            
            service_ticket = Service_ticket(
                VIN = "34433-VVV-343",
                service_date = date(2000,2,13),
                customer_id = customer.id
            )

            db.session.add(service_ticket)
            db.session.commit()


            service_ticket_id = service_ticket.id
            mechanic_id = mechanic.id



        response = self.client.put(f'/service_tickets/{service_ticket_id}/assign_mechanic/{mechanic_id}')
        self.assertEqual(response.status_code,200)
        self.assertIn(f"Mechanic {mechanic.id} assigned", response.json["Message"])


    def test_remove_mechanic_to_service_ticket(self):
        with self.app.app_context():

            customer = Customer(name="Jeanne Marie",
                                email="jm@gmail.com",
                                phone="07834303939393",
                                password="jm2025")

            db.session.add(customer)

            mechanic = Mechanic(name="Shimwa Jean Bosco",
                                email="sj@gmail.com",
                                phone="0783430393444",
                                salary="66,000")
            
            db.session.add(mechanic)
            db.session.commit()

            
            service_ticket = Service_ticket(
                VIN = "34433-VVV-343",
                service_date = date(2000,2,13),
                customer_id = customer.id
            )
            service_ticket.mechanics.append(mechanic)
            db.session.add(service_ticket)
            db.session.commit()


            service_ticket_id = service_ticket.id
            mechanic_id = mechanic.id



        response = self.client.put(f'/service_tickets/{service_ticket_id}/remove_mechanic/{mechanic_id}')
        self.assertEqual(response.status_code,200)
        self.assertIn(f"Mechanic {mechanic.id} removed from service ticket {service_ticket.id} successfully", response.json["Message"])

        







    

