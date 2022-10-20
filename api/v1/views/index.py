#!/usr/bin/python3
"""Index file"""

from flask import Flask
from api.v1.views import app_views

@app_views.route('/api/v1/status')
def status():
    """return a status code in JSON format"""
    return {"status": "OK"}
