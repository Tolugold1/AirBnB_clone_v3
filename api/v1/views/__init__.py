#!/usr/bin/python3
"""app_vies blueprint"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.cities import *
from api.v1.views.states import *
from api.v1.views.users import *
<<<<<<< HEAD
=======
from api.v1.views.amenities import *
>>>>>>> 05a98f274eb2d0102aab8706fea7f5ac9df2868e
from api.v1.views.places import *
