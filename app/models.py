# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import DeclarativeBase,Mapped, mapped_column
# from datetime import date
# from typing import List
# from flask_marshmallow import Marshmallow
# from marshmallow import ValidationError
# from sqlalchemy import select



# class Base(DeclarativeBase):
#   pass

# db = SQLAlchemy(model_class = Base)


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
#     db.Column('servticket_id', db.ForeignKey('service_tickets.id')),
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