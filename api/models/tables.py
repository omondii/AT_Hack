#!/usr/bin/env python3
"""
Database schema definition for user authentication

Rider Table: Captures riders details upon registration
"""
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func, Table, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
Base = declarative_base()

rider_contact = Table('rider_contact', Base.metadata,
    Column('riderId', String(255), ForeignKey('rider.riderId'), primary_key=True),
    Column('userId', String(255), ForeignKey('contacts.userId'), primary_key=True)
)

class Rider(Base):
    """ Riders table """
    __tablename__ = "rider"
    
    riderId = Column(String(255), primary_key=True)
    firstName = Column(String(100), nullable=False)
    lastName = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(15))
    location = Column(String(255), nullable=True)
    contacts = relationship('Contact', secondary=rider_contact, back_populates='riders')
    
    def __repr__(self):
        return '<Rider %r>' % self.riderId

class Contact(Base):
    __tablename__ = "contacts"
    
    userId = Column(String(255), primary_key=True)
    firstName = Column(String(100), nullable=False)
    lastName = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=False)
    is_emergency_contact = Column(Boolean, default=False)
    relationship_type = Column(String(50))
    riders = relationship('Rider', secondary=rider_contact, back_populates='contacts')