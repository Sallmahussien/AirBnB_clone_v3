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


@app_views.route('/places/<place_id>', methods=['GET'])
def get_places_by_id(place_id):
    """Return place based on a corresponding id"""
    places_by_id = storage.get(Place, place_id)
    if not places_by_id:
        abort(404)

    return make_response(jsonify(places_by_id.to_dict()), 200)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a place with specific id"""
    place_by_id = storage.get(Place, place_id)
    if not place_by_id:
        abort(404)

    place_by_id.delete()
    storage.save()

    return make_response({}, 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates new place"""
    city_by_id = storage.get(City, city_id)
    if not city_by_id:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        return make_response("Not a JSON", 400)
    if not body_request.get("user_id"):
        return make_response("Missing user_id", 400)
    if not body_request.get("name"):
        return make_response("Missing name", 400)

    user_by_id = storage.get(User, body_request.get('user_id'))
    if not user_by_id:
        abort(404)

    body_request["city_id"] = city_id
    place = Place(**body_request)
    place.save()

    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates a place with specific id"""
    place_by_id = storage.get(Place, place_id)
    if not place_by_id:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        return make_response("Not a JSON", 400)

    attributes_to_update = ['name', 'description', 'number_rooms',
                            'number_bathrooms', 'max_guest', 'price_by_night',
                            'latitude', 'longitude']

    for attribute in attributes_to_update:
        setattr(place_by_id, attribute,
                body_request.get(attribute, getattr(place_by_id, attribute)))
    storage.save()

    return make_response(jsonify(place_by_id.to_dict()), 200)
