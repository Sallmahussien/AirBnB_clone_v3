#!/usr/bin/python3
"""Implement places view"""


from flask import jsonify, abort, request

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """Get all places by specific city id."""
    cities = storage.all(City)
    city_by_id = cities.get('City.' + city_id)

    if not city_by_id:
        abort(404)

    place_list = [place.to_dict() for place in city_by_id.places]

    return jsonify(place_list), 200


@app_views.route('/places/<place_id>', methods=['GET'])
def get_places_by_id(place_id):
    """Return place based on a corresponding id"""
    places = storage.all(Place)
    places_by_id = places.get('Place.' + place_id)

    if not places_by_id:
        abort(404)

    return jsonify(places_by_id.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a place with specific id"""
    places = storage.all(Place)
    place_by_id = places.get('Place.' + place_id)
    if not place_by_id:
        abort(404)

    storage.delete(place_by_id)
    storage.save()

    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates new place"""
    cities = storage.all(City)
    city_by_id: City = cities.get('City.' + city_id)

    if not city_by_id:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")
    if "user_id" not in body_request.keys():
        abort(400, "Missing user_id")
    if "name" not in body_request.keys():
        abort(400, "Missing name")

    users = storage.all(User)
    user_by_id = users.get('User.' + body_request.get('user_id'))
    if not user_by_id:
        abort(404)

    place = Place(name=body_request.get('name'), city_id=city_by_id.id)
    storage.new(place)
    storage.save()

    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates a place with specific id"""
    places = storage.all(Place)
    place_by_id = places.get('Place.' + place_id)
    if not place_by_id:
        abort(404)

    body_request = request.get_json()

    if not body_request:
        abort(400, "Not a JSON")

    attributes_to_update = ['name', 'description', 'number_rooms',
                            'number_bathrooms', 'max_guest', 'price_by_night',
                            'latitude', 'longitude']

    for attribute in attributes_to_update:
        setattr(place_by_id, attribute,
                body_request.get(attribute, getattr(place_by_id, attribute)))

    storage.save()

    return jsonify(place_by_id.to_dict()), 200
