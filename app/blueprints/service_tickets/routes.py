from app.blueprints.service_tickets.schemas import service_ticket_schema,service_tickets_schema
from app.blueprints.service_tickets.schemas import edit_service_ticket_schema,return_service_ticket_schema
from app.models import Service_ticket,db
from app.models import Mechanic, Service_Inventory, Inventory
from flask import request,jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from . import service_tickets_bp

# Add an update route to your service_ticket blueprint to add and remove mechanics from a ticket.
# ---- PUT '/<int:ticket_id>/edit' : Takes in remove_ids, and add_ids
# ---- Use id's to look up the mechanic to append or remove them from the ticket.mechanics list


#===========Edit a ServiceTicket ===============================

@service_tickets_bp.route("/service_tickets/<int:service_ticket_id>",methods=["PUT"])
def edit_service_ticket(service_ticket_id):
  try:
    service_ticket_edits = edit_service_ticket_schema.load(request.json)
  except ValidationError as e:
    return jsonify(e.messages),400
  
  query = select(Service_ticket).where(Service_ticket.id ==service_ticket_id)
  service_ticket =db.session.execute(query).scalar()

  for mechanic_id in service_ticket_edits["add_mechanic_ids"]:
    query = select(Mechanic).where(Mechanic.id==mechanic_id)
    mechanic = db.session.execute(query).scalar()

    if mechanic and mechanic not in service_ticket.mechanics:
      service_ticket.mechanics.append(mechanic)
  
  for mechanic_id in service_ticket_edits["remove_mechanic_ids"]:
    query = select(Mechanic).where(Mechanic.id==mechanic_id)
    mechanic = db.session.execute(query).scalar()

    if mechanic and mechanic in service_ticket.mechanics:
      service_ticket.mechanics.remove(mechanic)
  db.session.commit()
  return return_service_ticket_schema.jsonify(service_ticket),200

@service_tickets_bp.route("/service_tickets/<int:service_ticket_id>/add_inventory",methods=['POST'])
def add_part_to_service_ticket(service_ticket_id):
  service_ticket = db.session.get(Service_ticket, service_ticket_id)
  if not service_ticket:
    return jsonify({"Error":"Service ticket not found"}),404
  
  data = request.json

  part_id = data.get('part_id')
  quantity = data.get('quantity')

  if not part_id or not quantity:
    return jsonify({"Error":"Part ID and quantity are required"}),400
  inventory_part = db.session.get(Inventory,part_id)
  if not inventory_part:
    return jsonify({"Error":"Part not found"}),404
  
  #Let's create association between service ticket and inventory part
  new_entry = Service_Inventory(service_ticket_id = service_ticket_id, part_id = part_id, quantity= quantity)

  db.session.add(new_entry)
  db.session.commit()

  return jsonify({
    "Message":"Part added to service ticket successfully",
    "service_ticket_id":service_ticket_id,
    "part_id":part_id,
    "quantity":quantity
    }),201

@service_tickets_bp.route("/service_tickets", methods=['POST'])
def create_service_ticket():
  try:
    service_ticket_data = service_ticket_schema.load(request.json)

  except ValidationError as e:
    return jsonify(e.messages),400
  
  query = select(Service_ticket).where(Service_ticket.VIN==service_ticket_data['VIN'])

  existing_service_ticket=db.session.execute(query).scalars().all()
  if existing_service_ticket:
    return jsonify({"Error":"This service ticket already exist in our database"}),400

  new_service_ticket = Service_ticket(**service_ticket_data)
  db.session.add(new_service_ticket)
  db.session.commit()
  return service_ticket_schema.jsonify(new_service_ticket),201

#=========Assigning Service tickets to mechanic============
@service_tickets_bp.route("/service_tickets/<int:service_ticket_id>/assign_mechanic/<int:mechanic_id>", methods=['PUT'])
def assign_mechanic_to_ticket(service_ticket_id, mechanic_id):
  service_ticket = db.session.get(Service_ticket, service_ticket_id)
  mechanic = db.session.get(Mechanic, mechanic_id)
  if not service_ticket or not mechanic:
    return jsonify({"Error":"Service Ticket or Mechanic not found"}),404
  if mechanic not in service_ticket.mechanics:
    service_ticket.mechanics.append(mechanic)
    db.session.commit

  db.session.commit()
  return jsonify({"Message": f"Mechanic {mechanic_id} assigned to service ticket {service_ticket_id}"})

#==========Removing Service tickets from mechanic=======================
@service_tickets_bp.route("/service_tickets/<int:service_ticket_id>/remove_mechanic/<int:mechanic_id>", methods=['PUT'])
def remove_mechanic_from_ticket(service_ticket_id, mechanic_id):
  service_ticket = db.session.get(Service_ticket, service_ticket_id)
  mechanic = db.session.get(Mechanic, mechanic_id)
  if not service_ticket or not mechanic:
    return jsonify({"Error":"Service Ticket or Mechanic not found"}),404
  if mechanic in service_ticket.mechanics:
    service_ticket.mechanics.remove(mechanic)
    db.session.commit

  db.session.commit()
  return jsonify({"Message": f"Mechanic {mechanic_id} removed from service ticket {service_ticket_id} successfully"})
  

#============GETTING ALL Service_ticketS======================
@service_tickets_bp.route("/service_tickets", methods=['GET'])
def get_service_tickets():
  query = select(Service_ticket)
  service_tickets = db.session.execute(query).scalars().all()
  return jsonify(service_tickets_schema.dump(service_tickets)),200

#==============RETRIEVE SPECIFIC Service_ticket=================

@service_tickets_bp.route("/service_tickets/<int:service_ticket_id>", methods=['GET'])

def get_Service_ticket(service_ticket_id):
  service_ticket = db.session.get(Service_ticket,service_ticket_id)

  if service_ticket:
    return service_ticket_schema.jsonify(service_ticket),200
  return jsonify({"Error": "Service_ticket not found"})

# #=============UPDATE A Service_ticket ========================

# @service_tickets_bp.route("/service_tickets/<int:service_ticket_id>", methods=['PUT'])

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

#=============DELETE Service_ticket ===========================
@service_tickets_bp.route("/service_tickets/<int:service_ticket_id>", methods=['DELETE'])

def delete_service_ticket(service_ticket_id):
  service_ticket = db.session.get(Service_ticket,service_ticket_id)

  if not service_ticket:
    return jsonify({"Error":"Service_ticket not found"})
  
  db.session.delete(service_ticket)
  db.session.commit()

  return jsonify({"Message":f"Service_ticket_id:{service_ticket_id}, has been successfully deleted"})