#!/usr/bin/python3
"""Index file"""

from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/status',  strict_slashes=False)
def status():
    """return a status code in JSON format"""
    return jsonify({"status": "OK"})

@app_views.route("/stats",  strict_slashes=False)
def stats():
    """
    Return the count of each 
    object in json format
    """

    objCount = {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")
            }

    return jsonify(objCount)
