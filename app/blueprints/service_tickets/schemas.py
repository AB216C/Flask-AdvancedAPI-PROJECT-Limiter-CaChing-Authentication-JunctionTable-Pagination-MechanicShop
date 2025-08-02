from app.extentions import ma
from app.models import Service_ticket
from marshmallow import fields


class Service_ticketSchema(ma.SQLAlchemyAutoSchema):
  mechanics = fields.Nested("MechanicSchema",many=True)
  customer = fields.Nested("CustomerSchema")
  mechanic_ids = fields.List(fields.Integer(),load_only=True)
  class Meta:
    model = Service_ticket
    include_fk = True
    fields = ("customer_id", "id", "mechanics", "customer", "mechanic_ids")


class Editservice_ticketSchema(ma.Schema):
  add_mechanic_ids = fields.List(fields.Integer(), required=True)
  remove_mechanic_ids = fields.List(fields.Integer(),required=True)
  class Meta:
    fields = ("add_mechanic_ids", "remove_mechanic_ids")

service_ticket_schema = Service_ticketSchema()
service_tickets_schema = Service_ticketSchema(many=True)
return_service_ticket_schema = Service_ticketSchema(exclude=["customer_id"])
edit_service_ticket_schema = Editservice_ticketSchema() 