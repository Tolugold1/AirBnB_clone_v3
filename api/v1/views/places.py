#!/usr/bin/python3
""" State objects API actiions """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<string:city_id>/places', methods=['GET'], strict_slashes=False)
def places_city(city_id):
    """ Retrieves the list of all Amenity objects """
    all_places = storage.all(Place)
    target_place = [obj.to_dict() for obj in all_places.values() if obj.city_id == city_id]
    if len(target_place) == 0:
        abort(404)
    return jsonify(target_place)


@app_views.route('/places/<string:place_id>', methods=['GET'], strict_slashes=False)
def r_place_id(place_id):
    """ Retrieves a Place object """
    onePlace = storage.get(Place, place_id)
    if not onePlace:
        abort(404)
    return jsonify(onePlace.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],strict_slashes=False)
def del_place(place_id):
    """ Deletes a Place object """
    onePlace = storage.get(Place, place_id)
    if not onePlace:
        abort(404)
    onePlace.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<string:city_id>/places', methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """ Creates a Place object """
    checkCity = storage.get(City, city_id)
    if not checkCity:
        abort(404)
    newPlace = request.get_json()
    if not newPlace:
        abort(400, "Not a JSON")
    if "user_id" not in newPlace:
        abort(400, "Missing user_id")
    checkUser = storage.get(User, newPlace["user_id"])
    if not checkUser:
        abort(404)
    if "name" not in newPlace:
        abort(400, "Missing name")
    place = Place(**newPlace)
    storage.new(place)

@app_views.route('/places/<string:place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """ Updates a place object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")

    for k, v in body_request.items():
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, k, v)

    storage.save()
    return make_response(jsonify(place.to_dict()), 200)