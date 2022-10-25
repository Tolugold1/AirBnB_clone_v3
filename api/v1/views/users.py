#!/usr/bin/python3
"""User view"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User

@app_views.route('/users', strict_slashes=False)
def all_users():
    """return all user"""
    all_users = []
    for user in storage.all(User).values():
        all_users.append(user.to_dict())
    return jsonify(all_users)

@app_views.route('/users/<user_id>', strict_slashes=False)
def users(user_id):
    """Retrieve all user and selected user"""

    if user_id is not None:
        user = storage.get(User, user_id)
        if not user:
            abort(404)
        return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """delete a user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return {}

@app_views.route("/users", methods=["POST"], strict_slashes=False)
def post_user():
    """create a new user"""
    n_user = request.get_json()
    if not n_user:
        abort(400, {"Not a JSON"})
    if 'email' not in n_user:
        abort(400, {"Missing email"})
    if 'password' not in n_user:
        abort(400, {"Missing password"})
    new_User = User(**n_user)
    storage.new(new_User)
    storage.save()
    return new_User.to_dict(), 201

@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """Update a user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user_update = request.get_json()
    if not user_update:
        abort(400, {"Not a JSON"})
    for k, v in user_update.items():
        setattr(user, k, v)
    storage.save()
    return jsonify(user.to_dict())
    
