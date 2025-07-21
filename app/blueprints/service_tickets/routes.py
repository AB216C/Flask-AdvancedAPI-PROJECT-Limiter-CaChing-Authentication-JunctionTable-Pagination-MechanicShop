from app.blueprints.service_tickets.schemas import service_ticket_schema,service_tickets_schema
from app.models import Service_ticket,db
from app.models import Mechanic
from flask import request,jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from . import service_tickets_bp


@service_tickets_bp.route("/service_tickets", methods=['POST']) #This a listener: As soon as it hears, this request, it fires the following function
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

#=========Assigning Service tickets to mechanics============
@service_tickets_bp.route("/service_tickets/<int:service_ticket_id>/assign_mechanics", methods=['POST'])
def assign_mechanics(service_ticket_id):
  service_ticket = db.session.get(Service_ticket, service_ticket_id)
  if not service_ticket:
    return jsonify({"Error":"Ticket not found"}),404
  mechanic_ids = request.json.get("mechanic_ids", [])
  mechanics = db.session.query(Mechanic).filter(Mechanic.id.in_(mechanic_ids)).all()
  service_ticket.mechanics = mechanics

  db.session.commit()
  return jsonify({"Message": "Mechanics assigned successfully"})
  

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

#=============UPDATE A Service_ticket ========================

@service_tickets_bp.route("/service_tickets/<int:service_ticket_id>", methods=['PUT'])

def update_service_ticket(service_ticket_id):
  service_ticket = db.session.get(Service_ticket,service_ticket_id)

  if not service_ticket:
    return jsonify({"Error":"Service_ticket not found"})
  
  try:
    service_ticket_data = service_ticket_schema.load(request.json)

  except ValidationError as e:
    return jsonify(e.messages),400
  
  for key,value in service_ticket_data.items():
    setattr(Service_ticket,key,value)

  db.session.commit()
  return service_ticket_schema.jsonify(service_ticket),200

#=============DELETE Service_ticket ===========================
@service_tickets_bp.route("/service_tickets/<int:Service_ticket_id>", methods=['DELETE'])

def delete_service_ticket(service_ticket_id):
  service_ticket = db.session.get(Service_ticket,service_ticket_id)

  if not service_ticket:
    return jsonify({"Error":"Service_ticket not found"})
  
  db.session.delete(service_ticket)
  db.session.commit()

  return jsonify({"Message":f"Service_ticket_id:{service_ticket_id}, has been successfully deleted"})