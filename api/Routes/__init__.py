#!/usr/bin/env python3
""" Module Blueprint collection and registration """
from flask import Blueprint

bp = Blueprint('auth', __name__)

from . import routes