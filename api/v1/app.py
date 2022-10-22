#!/usr/bin/python3
"""Flask app.py"""


from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)

@app.teardown_appcontext
def remove_session(response_or_exc):
    """Remove the surrent session"""
    storage.close()

if __name__ == '__main__':
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')
    if HBNB_API_HOST and HBNB_API_PORT:
        app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
    app.run(host='0.0.0.0', port=5001, threaded=True)
