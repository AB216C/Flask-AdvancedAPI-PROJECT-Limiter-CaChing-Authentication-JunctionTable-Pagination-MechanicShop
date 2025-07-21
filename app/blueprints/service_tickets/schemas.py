from app.extentions import ma
from app.models import Service_ticket

class Service_ticketSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Service_ticket
    include_fk = True

service_ticket_schema = Service_ticketSchema()
service_tickets_schema = Service_ticketSchema(many=True)