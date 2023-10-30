#!/usr/bin/python3
"""Implement places view"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """Get all places by specific city id."""
    city_by_id = storage.get(City, city_id)
    if not city_by_id:
        abort(404)

    place_list = [place.to_dict() for place in city_by_id.places]

    return make_response(jsonify(place_list), 200)
