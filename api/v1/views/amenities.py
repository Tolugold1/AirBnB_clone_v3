#!/usr/bin/python3
""" State objects API actiions """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    """ Retrieves the list of all Amenity objects """
    all_amenities = storage.all(Amenity)
    return jsonify([obj.to_dict() for obj in all_amenities.values()])


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'], strict_slashes=False)
def r_amenity_id(amenity_id):
    """ Retrieves a Amenity object """
    oneAmenity = storage.get(Amenity, amenity_id)
    if not oneAmenity:
        abort(404)
    return jsonify(oneAmenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],strict_slashes=False)
def del_amenity(amenity_id):
    """ Deletes a State object """
    oneAmenity = storage.get(Amenity, amenity_id)
    if not oneAmenity:
        abort(404)
    oneAmenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """ Creates a Amenity object """
    newAmenity = request.get_json()
    if not newAmenity:
        abort(400, "Not a JSON")
    if "name" not in newAmenity:
        abort(400, "Missing name")
    amenity = Amenity(**newAmenity)
    storage.new(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """ Updates a Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")

    for k, v in body_request.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, k, v)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
