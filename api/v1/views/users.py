#!/usr/bin/python3
"""Implement users view"""

from flask import jsonify, abort, request

from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def get_all_user():
    """Get all users from the storage."""
    users = storage.all(User)
    user_list = [value.to_dict() for value in users.values()]
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """Return user based on a corresponding id."""
    users = storage.all(User)
    user_by_id = users.get('User.' + user_id)
    if not user_by_id:
        abort(404)
    return jsonify(user_by_id.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a user with specific id."""
    users = storage.all(User)
    user_by_id = users.get('User.' + user_id)
    if not user_by_id:
        abort(404)

    storage.delete(user_by_id)
    storage.save()

    return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
def create_user():
    """Creates new user."""
    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")
    if "email" not in body_request.keys():
        abort(400, "Missing email")
    if "password" not in body_request.keys():
        abort(400, "Missing password")

    user = User(email=body_request.get('email'),
                password=body_request.get('password'))
    storage.new(user)
    storage.save()

    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a state with specific id."""
    users = storage.all(User)
    user_by_id = users.get('User.' + user_id)
    if not user_by_id:
        abort(404)

    body_request = request.get_json()

    if not body_request:
        abort(400, "Not a JSON")

    attributes_to_update = ['first_name', 'last_name', 'email', 'password']

    for attribute in attributes_to_update:
        setattr(user_by_id, attribute,
                body_request.get(attribute, getattr(user_by_id, attribute)))
    storage.save()

    return jsonify(user_by_id.to_dict()), 200
