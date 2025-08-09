from app.blueprints.customers.schemas import customer_schema,customers_schema,login_schema
from app.models import Customer,db
from flask import request,jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from . import customers_bp
from app.extentions import limiter,cache
from app.utils.util import encode_token,token_required

#=========GENERATING token after logging in using EMAIL and PASSWORD =================
@customers_bp.route("/customer/login", methods=['POST'])
def login():
    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Customer).where(Customer.email == email)
    customer = db.session.execute(query).scalars().first()  

    if customer and customer.password == password:
        token = encode_token(customer.id)
        response = {
            "status": "success",
            "message": "Login successful",
            "token": token
        }
        return jsonify(response), 200
    else:
        return jsonify({"Error": "Invalid email or password"})

#============CREATE A CUSTOMER =======================
@customers_bp.route("/customers", methods=['POST']) 
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

#============GETTING ALL CUSTOMERS AND APPLYING LIMITER AND CACHE TO THE ROUTE======================
# @customers_bp.route("/customers", methods=['GET'])
# @limiter.limit("5 per 30 seconds")
# @cache.cached(timeout=80)
# def get_customers():
#   query = select(Customer)
#   customers = db.session.execute(query).scalars().all()
#   return jsonify(customers_schema.dump(customers)),200

#==========Paginating customers ============================
@customers_bp.route("/customers", methods=['GET'])
@limiter.limit("5 per 30 seconds")
@cache.cached(timeout=80)
def get_paginated_customers():
   try:
      page = int(request.args.get('page'))
      per_page = int(request.args.get('per_page'))
      query = select(Customer)
      customers = db.paginate(query, page = page, per_page = per_page)
      return jsonify(customers_schema.dump(customers)),200
   except:
      query = select(Customer)
      customers = db.session.execute(query).scalars().all()
      return jsonify(customers_schema.dump(customers)),200

#==============RETRIEVE SPECIFIC CUSTOMER=================

@customers_bp.route("/customers/<int:customer_id>", methods=['GET'])
@limiter.limit("2 per 60 seconds")
@cache.cached(timeout=80)
def get_customer(customer_id):
  customer = db.session.get(Customer,customer_id)

  if customer:
    return customer_schema.jsonify(customer),200
  return jsonify({"Error": "Customer not found"})

#=============UPDATE A CUSTOMER ========================

@customers_bp.route("/customers/<int:customer_id>", methods=['PUT'])
@token_required

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
@token_required

def delete_customer(customer_id):
  customer = db.session.get(Customer,customer_id)

  if not customer:
    return jsonify({"Error":"Customer not found"})
  
  db.session.delete(customer)
  db.session.commit()

  return jsonify({"Message":f"Customer_id:{customer_id}, has been successfully deleted"})