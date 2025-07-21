from app.blueprints.customers.schemas import customer_schema,customers_schema
from app.models import Customer,db
from flask import request,jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from . import customers_bp


@customers_bp.route("/customers", methods=['POST']) #This a listener: As soon as it hears, this request, it fires the following function
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
@customers_bp.route("/customers", methods=['GET'])
def get_customers():
  query = select(Customer)
  customers = db.session.execute(query).scalars().all()
  return jsonify(customers_schema.dump(customers)),200

#==============RETRIEVE SPECIFIC CUSTOMER=================

@customers_bp.route("/customers/<int:customer_id>", methods=['GET'])

def get_customer(customer_id):
  customer = db.session.get(Customer,customer_id)

  if customer:
    return customer_schema.jsonify(customer),200
  return jsonify({"Error": "Customer not found"})

#=============UPDATE A CUSTOMER ========================

@customers_bp.route("/customers/<int:customer_id>", methods=['PUT'])

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
@customers_bp.route("/customers/<int:customer_id>", methods=['DELETE'])

def delete_customer(customer_id):
  customer = db.session.get(Customer,customer_id)

  if not customer:
    return jsonify({"Error":"Customer not found"})
  
  db.session.delete(customer)
  db.session.commit()

  return jsonify({"Message":f"Customer_id:{customer_id}, has been successfully deleted"})