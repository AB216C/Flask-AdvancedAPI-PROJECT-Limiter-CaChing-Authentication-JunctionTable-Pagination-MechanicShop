from app.blueprints.inventory.schemas import inventory_schema,inventories_schema
from app.models import Inventory,db
from flask import request,jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from . import inventory_bp

#============CREATE AN INVENTORY =======================

@inventory_bp.route("/inventory", methods=['POST']) 
def create_inventory():
  try:
    inventory_data = inventory_schema.load(request.json)

  except ValidationError as e:
    return jsonify(e.messages),400
  
  query = select(Inventory).where(Inventory.part_number==inventory_data['part_number'])

  existing_inventory=db.session.execute(query).scalars().all()
  if existing_inventory:
    return jsonify({"Error":"This part number is associated with existing account"}),400

  new_inventory = Inventory(**inventory_data)
  db.session.add(new_inventory)
  db.session.commit()
  return inventory_schema.jsonify(new_inventory),201

#============GETTING ALL inventory======================
@inventory_bp.route("/inventory", methods=['GET'])
def get_inventories():
  query = select(Inventory)
  inventory = db.session.execute(query).scalars().all()
  return jsonify(inventories_schema.dump(inventory)),200

#==============RETRIEVE SPECIFIC inventory=================

@inventory_bp.route("/inventory/<int:inventory_id>", methods=['GET'])

def get_inventory(inventory_id):
  inventory = db.session.get(Inventory,inventory_id)

  if inventory:
    return inventory_schema.jsonify(inventory),200
  return jsonify({"Error": "inventory not found"}),404

#=============UPDATE A inventory ========================

@inventory_bp.route("/inventory/<int:inventory_id>", methods=['PUT'])

def update_inventory(inventory_id):
  inventory = db.session.get(Inventory,inventory_id)

  if not inventory:
    return jsonify({"Error":"inventory not found"}),404
  
  try:
    inventory_data = inventory_schema.load(request.json)

  except ValidationError as e:
    return jsonify(e.messages),400
  
  for key,value in inventory_data.items():
    setattr(inventory,key,value)

  db.session.commit()
  return inventory_schema.jsonify(inventory),200

#=============DELETE inventory ===========================
@inventory_bp.route("/inventory/<int:inventory_id>", methods=['DELETE'])

def delete_inventory(inventory_id):
  inventory = db.session.get(Inventory,inventory_id)

  if not inventory:
    return jsonify({"Error":"inventory not found"}),404
  
  db.session.delete(inventory)
  db.session.commit()

  return jsonify({"Message":f"inventory_id:{inventory_id}, has been successfully deleted"})