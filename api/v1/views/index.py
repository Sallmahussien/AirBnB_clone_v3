#!/usr/bin/python3
"""Implement different routes"""

from api.v1.views import app_views

from flask import jsonify


@app_views.route('/status')
def status():
    """Return status: ok"""
    return jsonify({"status": "OK"})
