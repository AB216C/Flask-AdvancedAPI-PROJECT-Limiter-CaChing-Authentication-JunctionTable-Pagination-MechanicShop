from app import create_app
from app.models import db

app = create_app('DevelopmentConfig')

with app.app_context():
  db.create_all()

app.run()



# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import DeclarativeBase,Mapped, mapped_column
# from datetime import date
# from typing import List
# from flask_marshmallow import Marshmallow
# from marshmallow import ValidationError
# from sqlalchemy import select

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Mahirane231995@localhost/Shop'

# class Base(DeclarativeBase):
#   pass

# db = SQLAlchemy(model_class = Base)
# ma = Marshmallow()

# db.init_app(app)
# ma.init_app(app)

# class Customer(Base):
#   __tablename__ = 'customers'

#   id: Mapped[int] = mapped_column(primary_key=True)
#   name: Mapped[str] = mapped_column(db.String(255), nullable=False)
#   email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
#   phone: Mapped[str] = mapped_column(db.String(255), nullable=False)


#   service_tickets: Mapped[List['Service_ticket']] = db.relationship(back_populates='customer')

# service_mechanic = db.Table(
#     'service_mechanic',
#     Base.metadata,
#     db.Column('service_ticket_id', db.ForeignKey('service_tickets.id')),
#     db.Column('mechanic_id', db.ForeignKey('mechanics.id'))
# )

# class Service_ticket(Base):
#   __tablename__ = 'service_tickets'

#   id: Mapped[int] = mapped_column(primary_key=True)
#   VIN:Mapped[str] = mapped_column(db.String(255), nullable=False)
#   service_date: Mapped[date] = mapped_column(db.Date)
#   customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'))


#   customer: Mapped['Customer'] = db.relationship(back_populates='service_tickets')
#   mechanics: Mapped[List['Mechanic']] = db.relationship(secondary=service_mechanic, back_populates='service_tickets')


# class Mechanic(Base):
#     __tablename__ = "mechanics"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(db.String(255), nullable=False)
#     email: Mapped[str] = mapped_column(db.String(255), nullable=False)
#     phone: Mapped[str] = mapped_column(db.String(255), nullable=False)
#     salary: Mapped[str] = mapped_column(db.String(255), nullable=False)

#     service_tickets: Mapped[List['Service_ticket']] = db.relationship(secondary=service_mechanic, back_populates='mechanics')


# #================SCHEMAS================

# #======CUSTOMER SCHEMA===================
# class CustomerSchema(ma.SQLAlchemyAutoSchema):
#   class Meta:
#     model = Customer

# customer_schema = CustomerSchema()
# customers_schema = CustomerSchema(many=True)

# @app.route("/customers", methods=['POST']) #This a listener: As soon as it hears, this request, it fires the following function
# def create_customer():
#   try:
#     customer_data = customer_schema.load(request.json)

#   except ValidationError as e:
#     return jsonify(e.messages),400
  
#   query = select(Customer).where(Customer.email==customer_data['email'])

#   existing_customer=db.session.execute(query).scalars().all()
#   if existing_customer:
#     return jsonify({"Error":"This email is associated with existing account"}),400

#   new_customer = Customer(**customer_data)
#   db.session.add(new_customer)
#   db.session.commit()
#   return customer_schema.jsonify(new_customer),201

# #============GETTING ALL CUSTOMERS======================
# @app.route("/customers", methods=['GET'])
# def get_members():
#   query = select(Customer)
#   customers = db.session.execute(query).scalars().all()
#   return jsonify(customers_schema.dump(customers)),200

# #==============RETRIEVE SPECIFIC CUSTOMER=================

# @app.route("/customers/<int:customer_id>", methods=['GET'])

# def get_customer(customer_id):
#   customer = db.session.get(Customer,customer_id)

#   if customer:
#     return customer_schema.jsonify(customer),200
#   return jsonify({"Error": "Customer not found"})

# #=============UPDATE A CUSTOMER ========================

# @app.route("/customers/<int:customer_id>", methods=['PUT'])

# def update_customer(customer_id):
#   customer = db.session.get(Customer,customer_id)

#   if not customer:
#     return jsonify({"Error":"Customer not found"})
  
#   try:
#     customer_data = customer_schema.load(request.json)

#   except ValidationError as e:
#     return jsonify(e.messages),400
  
#   for key,value in customer_data.items():
#     setattr(customer,key,value)

#   db.session.commit()
#   return customer_schema.jsonify(customer),200

# #=============DELETE CUSTOMER ===========================
# @app.route("/customers/<int:customer_id>", methods=['DELETE'])

# def delete_customer(customer_id):
#   customer = db.session.get(Customer,customer_id)

#   if not customer:
#     return jsonify({"Error":"Customer not found"})
  
#   db.session.delete(customer)
#   db.session.commit()

#   return jsonify({"Message":f"Customer_id:{customer_id}, has been successfully deleted"})


# #======Mechanic SCHEMA===================

# class MechanicSchema(ma.SQLAlchemyAutoSchema):
#   class Meta:
#     model = Mechanic

# mechanic_schema = MechanicSchema()
# mechanics_schema = MechanicSchema(many=True)

# @app.route("/mechanics", methods=['POST']) #This a listener: As soon as it hears, this request, it fires the following function
# def create_mechanic():
#   try:
#     mechanic_data = mechanic_schema.load(request.json)

#   except ValidationError as e:
#     return jsonify(e.messages),400
  
#   query = select(Mechanic).where(Mechanic.email==mechanic_data['email'])

#   existing_mechanic=db.session.execute(query).scalars().all()
#   if existing_mechanic:
#     return jsonify({"Error":"This email is associated with existing account"}),400

#   new_mechanic = Mechanic(**mechanic_data)
#   db.session.add(new_mechanic)
#   db.session.commit()
#   return mechanic_schema.jsonify(new_mechanic),201

# #============GETTING ALL MechanicS======================
# @app.route("/mechanics", methods=['GET'])
# def get_mechanics():
#   query = select(Mechanic)
#   mechanics = db.session.execute(query).scalars().all()
#   return jsonify(mechanics_schema.dump(mechanics)),200

# #==============RETRIEVE SPECIFIC Mechanic=================

# @app.route("/mechanics/<int:mechanic_id>", methods=['GET'])

# def get_mechanic(mechanic_id):
#   mechanic = db.session.get(Mechanic,mechanic_id)

#   if mechanic:
#     return mechanic_schema.jsonify(mechanic),200
#   return jsonify({"Error": "Mechanic not found"})

# #=============UPDATE A Mechanic ========================

# @app.route("/mechanics/<int:mechanic_id>", methods=['PUT'])

# def update_mechanic(mechanic_id):
#   mechanic = db.session.get(Mechanic,mechanic_id)

#   if not mechanic:
#     return jsonify({"Error":"Mechanic not found"})
  
#   try:
#     mechanic_data = mechanic_schema.load(request.json)

#   except ValidationError as e:
#     return jsonify(e.messages),400
  
#   for key,value in mechanic_data.items():
#     setattr(Mechanic,key,value)

#   db.session.commit()
#   return mechanic_schema.jsonify(mechanic),200

# #=============DELETE Mechanic ===========================
# @app.route("/mechanics/<int:mechanic_id>", methods=['DELETE'])

# def delete_mechanic(mechanic_id):
#   mechanic = db.session.get(Mechanic,mechanic_id)

#   if not mechanic:
#     return jsonify({"Error":"Mechanic not found"})
  
#   db.session.delete(mechanic)
#   db.session.commit()

#   return jsonify({"Message":f"Mechanic_id:{mechanic_id}, has been successfully deleted"})


# #======SERVICE TICKETS SCHEMA===================

# #====CREATING SERVICE TICKETS================
# class Service_ticketSchema(ma.SQLAlchemyAutoSchema):
#   class Meta:
#     model = Service_ticket
#     include_fk = True

# service_ticket_schema = Service_ticketSchema()
# service_tickets_schema = Service_ticketSchema(many=True)

# @app.route("/service_tickets", methods=['POST']) #This a listener: As soon as it hears, this request, it fires the following function
# def create_service_ticket():
#   try:
#     service_ticket_data = service_ticket_schema.load(request.json)

#   except ValidationError as e:
#     return jsonify(e.messages),400
  
#   query = select(Service_ticket).where(Service_ticket.VIN==service_ticket_data['VIN'])

#   existing_service_ticket=db.session.execute(query).scalars().all()
#   if existing_service_ticket:
#     return jsonify({"Error":"This service ticket already exist in our database"}),400

#   new_service_ticket = Service_ticket(**service_ticket_data)
#   db.session.add(new_service_ticket)
#   db.session.commit()
#   return service_ticket_schema.jsonify(new_service_ticket),201

# #=========Assigning Service tickets to mechanics============
# @app.route("/service_tickets/<int:service_ticket_id>/assign_mechanics", methods=['POST'])
# def assign_mechanics(service_ticket_id):
#   service_ticket = db.session.get(Service_ticket, service_ticket_id)
#   if not service_ticket:
#     return jsonify({"Error":"Ticket not found"}),404
#   mechanic_ids = request.json.get("mechanic_ids", [])
#   mechanics = db.session.query(Mechanic).filter(Mechanic.id.in_(mechanic_ids)).all()
#   service_ticket.mechanics = mechanics

#   db.session.commit()
#   return jsonify({"Message": "Mechanics assigned successfully"})
  

# #============GETTING ALL Service_ticketS======================
# @app.route("/service_tickets", methods=['GET'])
# def get_service_tickets():
#   query = select(Service_ticket)
#   service_tickets = db.session.execute(query).scalars().all()
#   return jsonify(service_tickets_schema.dump(service_tickets)),200

# #==============RETRIEVE SPECIFIC Service_ticket=================

# @app.route("/service_tickets/<int:service_ticket_id>", methods=['GET'])

# def get_Service_ticket(service_ticket_id):
#   service_ticket = db.session.get(Service_ticket,service_ticket_id)

#   if service_ticket:
#     return service_ticket_schema.jsonify(service_ticket),200
#   return jsonify({"Error": "Service_ticket not found"})

# #=============UPDATE A Service_ticket ========================

# @app.route("/service_tickets/<int:service_ticket_id>", methods=['PUT'])

# def update_service_ticket(service_ticket_id):
#   service_ticket = db.session.get(Service_ticket,service_ticket_id)

#   if not service_ticket:
#     return jsonify({"Error":"Service_ticket not found"})
  
#   try:
#     service_ticket_data = service_ticket_schema.load(request.json)

#   except ValidationError as e:
#     return jsonify(e.messages),400
  
#   for key,value in service_ticket_data.items():
#     setattr(Service_ticket,key,value)

#   db.session.commit()
#   return service_ticket_schema.jsonify(service_ticket),200

# #=============DELETE Service_ticket ===========================
# @app.route("/service_tickets/<int:Service_ticket_id>", methods=['DELETE'])

# def delete_service_ticket(service_ticket_id):
#   service_ticket = db.session.get(Service_ticket,service_ticket_id)

#   if not service_ticket:
#     return jsonify({"Error":"Service_ticket not found"})
  
#   db.session.delete(service_ticket)
#   db.session.commit()

#   return jsonify({"Message":f"Service_ticket_id:{service_ticket_id}, has been successfully deleted"})


# with app.app_context():
#   db.create_all()

# app.run(debug=True)