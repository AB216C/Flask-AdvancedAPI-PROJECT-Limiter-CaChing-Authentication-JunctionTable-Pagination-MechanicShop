from app.blueprints.mechanics.schemas import mechanic_schema,mechanics_schema
from app.models import Mechanic,db
from flask import request,jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from . import mechanics_bp


@mechanics_bp.route("/mechanics", methods=['POST']) #This a listener: As soon as it hears, this request, it fires the following function
def create_mechanic():
  try:
    mechanic_data = mechanic_schema.load(request.json)

  except ValidationError as e:
    return jsonify(e.messages),400
  
  query = select(Mechanic).where(Mechanic.email==mechanic_data['email'])

  existing_mechanic=db.session.execute(query).scalars().all()
  if existing_mechanic:
    return jsonify({"Error":"This email is associated with existing account"}),400

  new_mechanic = Mechanic(**mechanic_data)
  db.session.add(new_mechanic)
  db.session.commit()
  return mechanic_schema.jsonify(new_mechanic),201

#============GETTING ALL MechanicS======================
@mechanics_bp.route("/mechanics", methods=['GET'])
def get_mechanics():
  query = select(Mechanic)
  mechanics = db.session.execute(query).scalars().all()
  return jsonify(mechanics_schema.dump(mechanics)),200

#==============RETRIEVE SPECIFIC Mechanic=================

@mechanics_bp.route("/mechanics/<int:mechanic_id>", methods=['GET'])

def get_mechanic(mechanic_id):
  mechanic = db.session.get(Mechanic,mechanic_id)

  if mechanic:
    return mechanic_schema.jsonify(mechanic),200
  return jsonify({"Error": "Mechanic not found"})

#=============UPDATE A Mechanic ========================

@mechanics_bp.route("/mechanics/<int:mechanic_id>", methods=['PUT'])

def update_mechanic(mechanic_id):
  mechanic = db.session.get(Mechanic,mechanic_id)

  if not mechanic:
    return jsonify({"Error":"Mechanic not found"})
  
  try:
    mechanic_data = mechanic_schema.load(request.json)

  except ValidationError as e:
    return jsonify(e.messages),400
  
  for key,value in mechanic_data.items():
    setattr(Mechanic,key,value)

  db.session.commit()
  return mechanic_schema.jsonify(mechanic),200

#=============DELETE Mechanic ===========================
@mechanics_bp.route("/mechanics/<int:mechanic_id>", methods=['DELETE'])

def delete_mechanic(mechanic_id):
  mechanic = db.session.get(Mechanic,mechanic_id)

  if not mechanic:
    return jsonify({"Error":"Mechanic not found"})
  
  db.session.delete(mechanic)
  db.session.commit()

  return jsonify({"Message":f"Mechanic_id:{mechanic_id}, has been successfully deleted"})