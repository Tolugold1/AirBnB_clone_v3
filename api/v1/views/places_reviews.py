#!/usr/bin/python3
"""State view"""
from flask import Flask, jsonify, abort, request, make_response
from AirBnB_clone_v3.models import review
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review

@app_views.route("/places/<place_id>/reviews", strict_slashes=False)
def all_reviews(place_id):
    """Retrieve"""
    r = []
    if not storage.get(Place, place_id):
        abort(404)
    for review in storage.all(Review).values():
        if place_id == review.to_dict()['place_id']:
            r.append(review.to_dict())
    return jsonify(r)

@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review(review_id):
    """get a review"""
    r = storage.get(Review, review_id)
    if not r:
        abort(404)
    else:
        return jsonify(r)

@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """delete a review"""
    r = storage.get(Review, review_id)
    if not r:
        abort(404)
    else:
        storage.delete(r)
        storage.save()
        return {}

@app_views.route("/places/<place_id>/reviews", methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """create a new review"""
    place = storage.get(Place, place_id)
    n_review = request.get_json()
    if not place:
        abort(404)
    if not n_review:
        abort(400, {"Not a JSON"})
    if 'user_id' not in n_review:
        abort(400, {"Missing user_id"})
    if not storage.get('User', n_review['user_id']):
        abort(404)
    if 'text' not in n_review:
        abort(400, {"Missing text"})
    n_review['place_id'] = place_id
    new_review = Review(**n_review)
    storage.new(new_review)
    storage.save()
    return new_review.to_dict(), 201

@app_views.route('/reviews/<review_id>', methods=["PUT"], strict_slashes=False)
def put_review(review_id):
    """Update a review"""
    n_review = request.get_json()
    r = storage.get(Review, review_id)
    if not r:
        abort(404)
    if not n_review:
        abort(400, {"Not a JSON"})
    for k, v in n_review.items():
        if k not in ['id', 'user_id', 'place_id', 'created_at']:
            setattr(r, k, v)
    storage.save()
    return r.to_json()
