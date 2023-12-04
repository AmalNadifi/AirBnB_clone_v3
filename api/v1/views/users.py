#!/usr/bin/python3
"""
Create a view for State objects that handles all default RESTFul API actions
"""
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """ retrieves list of all user objects """
    users = storage.all(User).values()
    list_users = [user.to_dict() for user in users]
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_id(user_id):
    """ retrieves a user object identified with id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ deletes a user object and returns an empty dictionary """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """ creates User using POST method """
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    if content.get("email") is None:
        abort(400, 'Missing email')
    if content.get("password") is None:
        abort(400, 'Missing password')
    new_user = User(**content)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """ updtaes a user object with id using PUT method """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    content = request.get_json()
    list_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, val in content.items():
        if key not in list_keys:
            setattr(user, key, val)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
