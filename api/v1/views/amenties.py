#!/usr/bin/python3
"""Implement amenities view"""

from flask import jsonify, abort, request

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def get_all_amenities():
    """Get all amenities from the storage."""
    amenities = storage.all(Amenity)
    amenity_list = [value.to_dict() for value in amenities.values()]
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity_by_id(amenity_id):
    """Return amenity based on a corresponding id."""
    amenities = storage.all(Amenity)
    amenity_by_id = amenities.get('Amenity.' + amenity_id)
    if not amenity_by_id:
        abort(404)
    return jsonify(amenity_by_id.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes an amenity with specific id"""
    amenities = storage.all(Amenity)
    amenity_by_id = amenities.get('Amenity.' + amenity_id)
    if not amenity_by_id:
        abort(404)

    storage.delete(amenity_by_id)
    storage.save()

    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """Creates new amenity."""
    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")
    if "name" not in body_request.keys():
        abort(400, "Missing name")

    amenity = Amenity(name=body_request.get('name'))
    storage.new(amenity)
    storage.save()

    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Updates an amenity with specific id"""
    amenities = storage.all(Amenity)
    amenity_by_id = amenities.get('Amenity.' + amenity_id)
    if not amenity_by_id:
        abort(404)

    body_request = request.get_json()

    if not body_request:
        abort(400, "Not a JSON")

    amenity_by_id.name = body_request.get('name', amenity_by_id.name)
    storage.save()

    return jsonify(amenity_by_id.to_dict()), 200