#!/usr/bin/python3
"""Implement states view"""

from flask import jsonify, abort, request

from api.v1.views import app_views

from models.base_model import BaseModel
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_states():
    """Get all states from the storage"""
    states = storage.all(State)

    states_list = [BaseModel.to_dict(state) for state in states.values()]

    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Return state based on a coresponding id"""
    states = storage.all(State)

    id = "State." + state_id
    if id not in states.keys():
        abort(404)

    return jsonify(BaseModel.to_dict(states.get(id)))


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a state with specific id"""
    states = storage.all(State)

    id = "State." + state_id
    if id not in states.keys():
        abort(404)

    storage.delete(states.get(id))
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
    storage.new(new_state)
    storage.save()

    return jsonify(BaseModel.to_dict(new_state)), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Update an existing state"""
    states = storage.all(State)

    id = "State." + state_id
    if id not in states.keys():
        abort(404)

    body_request = request.get_json()

    if not body_request:
        abort(400, 'Not a JSON')

    updated_state = states.get(id)
    updated_state.name = body_request.get('name', updated_state.name)

    storage.save()

    return jsonify(BaseModel.to_dict(updated_state)), 200
