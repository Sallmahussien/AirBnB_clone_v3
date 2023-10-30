#!/usr/bin/python3
"""Implement states view"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_states():
    """get a list of states"""
    states = [obj.to_dict() for obj in storage.all(State).values()]
    return make_response(jsonify(states), 200)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Return state based on a coresponding id"""
    state_by_id: State = storage.get(State, state_id)
    if not state_by_id:
        abort(404)

    return jsonify(state_by_id.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a state with specific id"""
    state_by_id: State = storage.get(State, state_id)
    if not state_by_id:
        abort(404)

    state_by_id.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    """Creates new state"""
    body_request = request.get_json()

    if not body_request:
        abort(400, 'Not a JSON')

    if not body_request.get('name'):
        abort(400, 'Missing name')

    new_state = State(name=body_request.get('name'))
    new_state.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Update an existing state"""
    state_by_id: State = storage.get(State, state_id)
    if not state_by_id:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, 'Not a JSON')

    state_by_id.name = body_request.get('name', state_by_id.name)
    state_by_id.save()

    return jsonify(state_by_id.to_dict()), 200
