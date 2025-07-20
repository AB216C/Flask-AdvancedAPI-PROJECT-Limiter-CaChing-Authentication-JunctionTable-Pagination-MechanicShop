from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase,Mapped, mapped_column
from datetime import date
from typing import List
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from sqlalchemy import select


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Mahirane231995@localhost/Shop'

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class = Base)
ma = Marshmallow()

db.init_app(app)
ma.init_app(app)

class Customer(Base):
  __tablename__ = 'customers'

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(db.String(255), nullable=False)
  email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
  phone: Mapped[str] = mapped_column(db.String(255), nullable=False)


  service_tickets: Mapped[List['Service_ticket']] = db.relationship(back_populates='customer')

service_mechanic = db.Table(
    'service_mechanic',
    Base.metadata,
    db.Column('servticket_id', db.ForeignKey('service_tickets.id')),
    db.Column('mechanic_id', db.ForeignKey('mechanics.id'))
)

class Service_ticket(Base):
  __tablename__ = 'service_tickets'

  id: Mapped[int] = mapped_column(primary_key=True)
  VIN:Mapped[str] = mapped_column(db.String(255), nullable=False)
  service_date: Mapped[date] = mapped_column(db.Date)
  customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'))


  customer: Mapped['Customer'] = db.relationship(back_populates='service_tickets')
  mechanics: Mapped[List['Mechanic']] = db.relationship(secondary=service_mechanic, back_populates='service_tickets')


class Mechanic(Base):
    __tablename__ = "mechanics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(255), nullable=False)
    salary: Mapped[str] = mapped_column(db.String(255), nullable=False)

    service_tickets: Mapped[List['Service_ticket']] = db.relationship(secondary=service_mechanic, back_populates='mechanics')


#================SCHEMAS================

#======CUSTOMER SCHEMA===================
class CustomerSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Customer

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

@app.route("/customers", methods=['POST']) #This a listener: As soon as it hears, this request, it fires the following function
def create_customer():
  try:
    customer_data = customer_schema.load(request.json)

  except ValidationError as e:
    return jsonify(e.messages),400
  
  query = select(Customer).where(Customer.email==customer_data['email'])

  existing_customer=db.session.execute(query).scalars().all()
  if existing_customer:
    return jsonify({"Error":"This email is associated with existing account"}),400

  new_customer = Customer(**customer_data)
  db.session.add(new_customer)
  db.session.commit()
  return customer_schema.jsonify(new_customer),201

#============GETTING ALL CUSTOMERS======================
@app.route("/customers", methods=['GET'])
def get_members():
  query = select(Customer)
  customers = db.session.execute(query).scalars().all()
  return jsonify(customers_schema.dump(customers)),200

#==============RETRIEVE SPECIFIC CUSTOMER=================

@app.route("/customers/<int:customer_id>", methods=['GET'])

def get_customer(customer_id):
  customer = db.session.get(Customer,customer_id)

  if customer:
    return customer_schema.jsonify(customer),200
  return jsonify({"Error": "Customer not found"})

#=============UPDATE A CUSTOMER ========================

@app.route("/customers/<int:customer_id>", methods=['PUT'])

def update_customer(customer_id):
  customer = db.session.get(Customer,customer_id)

  if not customer:
    return jsonify({"Error":"Customer not found"})
  
  try:
    customer_data = customer_schema.load(request.json)

  except ValidationError as e:
    return jsonify(e.messages),400
  
  for key,value in customer_data.items():
    setattr(customer,key,value)

  db.session.commit()
  return customer_schema.jsonify(customer),200

#=============DELETE CUSTOMER ===========================
@app.route("/customers/<int:customer_id>", methods=['DELETE'])

def delete_customer(customer_id):
  customer = db.session.get(Customer,customer_id)

  if not customer:
    return jsonify({"Error":"Customer not found"})
  
  db.session.delete(customer)
  db.session.commit()

  return jsonify({"Message":f"Customer_id:{customer_id}, has been successfully deleted"})


with app.app_context():
  db.create_all()

app.run(debug=True)