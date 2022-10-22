#!/usr/bin/python3
"""Index file"""

from flask import Flask, jsonify
from api.v1.views import app_views

@app_views.route('/status')
def status():
    """return a status code in JSON format"""
    return jsonify({"status": "OK"})
