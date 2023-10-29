#!/usr/bin/python3
"""Implement cities view"""


from flask import jsonify, abort, request

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_city_by_state_id(state_id):
    """Get all cities from the storage based on a state id"""
    state_by_id: State = storage.get(State, state_id)

    if not state_by_id:
        abort(404)

    city_list = [city.to_dict() for city in state_by_id.cities]

    return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Return city based on a corresponding id"""
    city_by_id: City = storage.get(City, city_id)

    if not city_by_id:
        abort(404)

    return jsonify(city_by_id.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a city with specific id"""
    city_by_id: City = storage.get(City, city_id)

    if not city_by_id:
        abort(404)

    city_by_id.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Creates new city"""
    state_by_id: State = storage.get(State, state_id)

    if not state_by_id:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")
    if "name" not in body_request.keys():
        abort(400, "Missing name")

    city = City(name=body_request.get('name'), state_id=state_id)
    city.save()

    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Update an existing city"""
    city_by_id: City = storage.get(City, city_id)

    if not city_by_id:
        abort(404)

    body_request = request.get_json()

    if not body_request:
        abort(400, "Not a JSON")

    for key, value in request.get_json().items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city_by_id, key, value)
    city_by_id.save()

    return jsonify(city_by_id.to_dict()), 200
