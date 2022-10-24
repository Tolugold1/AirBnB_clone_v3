#!/usr/bin/python3
"""State view"""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User

@app_views.route("/cities/<city_id>/places", 
                 strict_slashes=False)
def all_place(city_id):
    """retrieve all places"""
    city = storage.get(City, city_id)
    places = []
    if not city:
        abort(404)
    for place in storage.all(Place).values():
        places.append(place.to_dict())
    return make_response(jsonify(places))

@app_views.route("/places/<place_id>", 
                 strict_slashes=False)
def id_place(place_id):
    """Retrieves a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return make_response(jsonify(place.to_dict()))

@app_views.route('/places/<place_id>', methods=['DELETE'], 
                 strict_slashes=False)
def delete_place(place_id):
    """delete a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route("/cities/<city_id>/places", methods=['POST'], 
                 strict_slashes=False)
def new_place(city_id):
    """Create a new place"""
    n_place = request.get_json()
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not n_place:
        abort(400, {"Not a JSON"})
    elif 'user_id' not in n_place:
        abort(400, {"Missing user_id"})
    elif not storage.get('User', n_place['user_id']):
        abort(400)
    elif 'name' not in n_place:
        abort(400, {"Missing name"})
    n_place['city_id'] = city_id
    nw_place = Place(**n_place)
    storage.new(nw_place)
    storage.save()
    return make_response(jsonify(nw_place.to_dict()), 201)

@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """update a place"""
    place = storage.get(Place, place_id)
    u_place = request.get_json()
    if not place:
        abort(404)
    if not u_place:
        abort(400, {"Not a JSON"})
    for k, v in u_place.items():
        if k not in ['id', 'user_id', 'city_id', 'created_at',
                     'updated_at']:
            setattr(place, k, v)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
