#!/usr/bin/env python3
""" App routes """
import uuid
from flask import request, jsonify, abort
from models import storage
from models.tables import Rider, Contact
from werkzeug.security import generate_password_hash
from werkzeug.exceptions import BadRequest, Conflict
from Routes import bp

@bp.route('/register', methods=['POST'])
def register():
    """ Adds a rider and emergency contact details to the db. """
    data = request.get_json()

    try:
        firstName = data.get('firstName')
        lastName = data.get('lastName')
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone')
        ct_firstname = data.get('eme_firstName')
        ct_lastname = data.get('eme_lastName')
        ct_phone = data.get('eme_phone')
        relationship = data.get('relationship')


        # Validate input
        if not all([firstName, lastName, email, password, phone,
                    ct_firstname, ct_lastname, ct_phone, relationship]):
            return jsonify({
                "status": "Bad request",
                "message": "All fields are required",
                "statusCode": 400
            }), 400

        # Check if user exists
        existing_user = storage.get_by_email(Rider, email)
        if existing_user:
            return jsonify({
                "status": "Conflict",
                "message": "User Exists!",
                "statusCode": 409
            }), 409

        # Hash the password
        if not password:
            return jsonify({"error": "Password is required"}), 400
        
        hashed_password = generate_password_hash(password)

        # Create a new Rider
        rider = Rider(
            riderId=str(uuid.uuid4()),
            firstName=firstName,
            lastName=lastName,
            email=email,
            password=hashed_password,
            phone=phone
        )

        # Create a related Contact
        contact = Contact(
            contactId=str(uuid.uuid4()),
            riderId=rider.riderId, 
            firstName=ct_firstname,
            lastName=ct_lastname,
            phone=ct_phone,
            relationship_type=relationship,
            is_emergency_contact=True
        )
        print("Received Data:", data)

        storage.new(rider)
        storage.new(contact)

        
        rider.contacts.append(contact)

        storage.save()

        return jsonify({
            "status": "success",
            "message": "Registration successful",
            "statusCode": 201,
            "data": {
                "user": {
                    "riderId": rider.riderId,
                    "firstName": rider.firstName,
                    "lastName": rider.lastName,
                    "email": rider.email,
                    "phone": rider.phone,
                    "contact_firstname": contact.firstName,
                    "contact_phone": contact.phone
                }
            }
        }), 201
    except Exception as e:
        storage.rollback()
        return jsonify({
            "status": "Bad Request",
            "message": str(e),
            "statusCode": 400
        }), 400

