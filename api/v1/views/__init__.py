#!/usr/bin/python3
"""app_vies blueprint"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, template_folder="templates")
from api.v1.views.index import *
