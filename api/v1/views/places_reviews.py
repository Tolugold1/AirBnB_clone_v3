#!/usr/bin/python3
"""Review view"""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review

@app_views.route("/places/<place_id>/reviews", strict_slashes=False)
def all_reviews(place_id):
    """ Retrieves the list of all Review objects """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])

@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review(review_id):
    """get a review"""
    r = storage.get(Review, review_id)
    if not r:
        abort(404)
    return jsonify(r.to_dict())

@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """delete a review"""
    r = storage.get(Review, review_id)
    if not r:
        abort(404)
    storage.delete(r)
    storage.save()
    return jsonify({}), 200

@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """ Creates a Review object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    new_review = request.get_json()
    if not new_review:
        abort(400, "Not a JSON")
    if "user_id" not in new_review:
        abort(400, "Missing user_id")
    user_id = new_review['user_id']
    if not storage.get(User, user_id):
        abort(404)
    if "text" not in new_review:
        abort(400, "Missing text")
    review = Review(**new_review)
    setattr(review, 'place_id', place_id)
    storage.new(review)
    storage.save()
    return make_response(jsonify(review.to_dict()), 201)

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
    return jsonify(r.to_dict())
