#!/usr/bin/env python3
"""
Database schema definition for user authentication

Rider Table: Captures riders details upon registration
"""
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func, Table, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy import event
import uuid
from services.sms_service import SMSService


Base = declarative_base()

rider_contact = Table('rider_contact', Base.metadata,
    Column('riderId', String(255), ForeignKey('riders.riderId'), primary_key=True),
    Column('contactId', String(255), ForeignKey('contacts.contactId'), primary_key=True)
)

class Rider(Base):
    """ Riders table """
    __tablename__ = "riders"
    
    riderId = Column(String(255), primary_key=True)
    firstName = Column(String(100), nullable=False)
    lastName = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(15))
    location = Column(String(255), nullable=True)

    contacts = relationship('Contact', back_populates='rider', cascade="all, delete-orphan")
    
    def __repr__(self):
        return '<Rider %r>' % self.riderId

class Contact(Base):
    __tablename__ = "contacts"
    
    contactId = Column(String, primary_key=True, default=str(uuid.uuid4()))
    riderId = Column(String, ForeignKey('riders.riderId'), nullable=False)
    firstName = Column(String(100), nullable=False)
    lastName = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=False)
    is_emergency_contact = Column(Boolean, default=False)
    relationship_type = Column(String(50), nullable=False)

    rider = relationship('Rider', back_populates='contacts')

    @classmethod
    def _declare_last_(cls):
        event.listen(Rider,'after_insert', SMSService.emergency_contact_confirmation)