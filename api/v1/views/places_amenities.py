#!/usr/bin/python3
"""Implement places_amenities view"""

from flask import abort, jsonify

from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_amenities_by_place_id(place_id):
    """Get amenities by place id"""
    place_by_id = storage.get(Place, place_id)

    if not place_by_id:
        abort(404)

    amenities_list = [amenity.to_dict() for amenity in place_by_id.amenities]

    return jsonify(amenities_list), 200
