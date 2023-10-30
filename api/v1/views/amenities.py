#!/usr/bin/python3
"""Implement amenities view"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def get_all_amenities():
    """Get all amenities from the storage."""
    amenities = storage.all(Amenity)
    amenity_list = [value.to_dict() for value in amenities.values()]
    return make_response(jsonify(amenity_list), 200)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity_by_id(amenity_id):
    """Return amenity based on a corresponding id."""
    amenity_by_id = storage.get(Amenity, amenity_id)
    if not amenity_by_id:
        abort(404)
    return make_response(jsonify(amenity_by_id.to_dict()), 200)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes an amenity with specific id"""
    amenity_by_id = storage.get(Amenity, amenity_id)
    if not amenity_by_id:
        abort(404)

    amenity_by_id.delete()
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """Creates new amenity."""
    body_request = request.get_json()
    if not body_request:
        return make_response(400, "Not a JSON")
    if "name" not in body_request.keys():
        return make_response(400, "Missing name")

    new_amenity = Amenity(**body_request)
    new_amenity.save()

    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Updates an amenity with specific id"""
    amenity_by_id = storage.get(Amenity, amenity_id)
    if not amenity_by_id:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        return make_response(400, "Not a JSON")

    setattr(amenity_by_id, 'name', body_request.get('name'))
    storage.save()

    return make_response(jsonify(amenity_by_id.to_dict()), 200)
