#!/usr/bin/python3
""" State objects API actiions """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """ Retrieves the list of all State objects """
    all_states = storage.all(State)
    return jsonify([obj.to_dict() for obj in all_states.values()])


@app_views.route('/states/<string:state_id>', methods=['GET'], strict_slashes=False)
def r_state_id(state_id):
    """ Retrieves a State object """
    oneState = storage.get(State, state_id)
    if not oneState:
        abort(404)
    return jsonify(oneState.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],strict_slashes=False)
def del_state(state_id):
    """ Deletes a State object """
    oneState = storage.get(State, state_id)
    if not oneState:
        abort(404)
    oneState.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ Creates a State object """
    newState = request.get_json()
    if not newState:
        abort(400, "Not a JSON")
    if "name" not in newState:
        abort(400, "Missing name")
    state = State(**newState)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ Updates a State object """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")

    for k, v in body_request.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, v)

    storage.save()
    return make_response(jsonify(state.to_dict()), 200)