#!/usr/bin/python3
"""city view"""
from flask import Flask, jsonify, abort, request
from models.city import City
from api.v1.views import app_views
from models import storage
from models.state import State

@app_views.route('/api/v1/states/<state_id>/cities', strict_slashes=False)
def city(state_id):
    """Retrieves the list of all City objects of a State"""
    allState_city = []
    if not storage.get('State', state_id):
        abort(404)
    for city in storage.all(City).items():
        if state_id == city.to_dict()['state_id']:
            allState_city.append(city.to_dict().values())
    return jsonify(allState_city)

@app_views.route('GET /api/v1/cities/<city_id>', strict_slashes=False)
def city_obj(city_id):
    """Retrieves a City object"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    else:
        return city.to_dict()
    
@app_views.route('/api/v1/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """DElete a city object"""
    empty_dict = {}
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return empty_dict
        
@app_views.route('/api/v1/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def post_new_city(state_id):
    """create new city under the specified state_id"""
    city_body_req = request.get_json()
    if not storage.get('State', state_id):
        abort(404)
    if not city_body_req:
        abort(400, {"Not a JSON"})
    if 'name' not in city_body_req:
        abort(400, {"Name not found"})
    city_body_req['state_id'] = state_id
    newCity = City(**city_body_req)
    storage.new(newCity)
    storage.save()
    return newCity.to_dict(), 201

@app_views.route('/api/v1/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """update existing city in the db or storage"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    updates = request.get_json()
    if not updates:
        abort(400, {"Not a JSON"})
    for k, v in city.items():
        setattr(city, k, v)
    return updates.to_dict()
