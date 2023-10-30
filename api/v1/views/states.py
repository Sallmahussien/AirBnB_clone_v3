#!/usr/bin/python3
"""Implement states view"""

from flask import jsonify, abort, request

from api.v1.views import app_views

from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_states():
    """Get all states from the storage"""
    states = storage.all(State)

    states_list = [state.to_dict() for state in states.values()]

    return jsonify(states_list), 200


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
