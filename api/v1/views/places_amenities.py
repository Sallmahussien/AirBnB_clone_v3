#!/usr/bin/python3
"""Implement places_amenities view"""

from api.v1.views import app_views
from flask import abort, jsonify

from models import storage
from models.place import Place, place_amenity
from models.amenity import Amenity

@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_amenities_by_place_id(place_id):
    """Get amenties by place id"""
    place_by_id: Place = storage.get(Place, place_id)

    if not place_by_id:
        abort(404)

    amenties_list = [amenity.to_dict() for amenity in place_by_id.amenities]

    return jsonify(amenties_list), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenties(place_id, amenity_id):
    """Deletes a Amenity object to a Place"""
    place_by_id: Place = storage.get(Place, place_id)

    if not place_by_id:
        abort(404)

    amenity_by_id: Amenity = storage.get(Amenity, amenity_id)
    if not amenity_by_id:
        abort(404)

    if amenity_by_id not in place_by_id.amenities:
        abort(404)

    storage.delete(amenity_by_id)
    storage.save()

    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def link_amenity_to_place(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    place_by_id: Place = storage.get(Place, place_id)

    if not place_by_id:
        abort(404)

    amenity_by_id: Amenity = storage.get(Amenity, amenity_id)
    if not amenity_by_id:
        abort(404)

    if amenity_by_id in place_by_id.amenities:
        return jsonify(amenity_by_id), 200
    
    place_by_id.amenities.append(amenity_by_id)
    place_by_id.save()

    return jsonify(amenity_by_id), 201
