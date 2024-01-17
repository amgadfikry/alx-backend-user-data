#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
auth_env = getenv('AUTH_TYPE')
if auth_env and auth_env == 'basic_auth':
    auth = BasicAuth()
elif auth_env and auth_env == 'session_auth':
    auth = SessionAuth()
elif auth_env and auth_env == 'session_exp_auth':
    auth = SessionExpAuth()
else:
    auth = Auth()

excluded_list = ['/api/v1/status/',
                 '/api/v1/unauthorized/',
                 '/api/v1/forbidden/'
                 '/api/v1/auth_session/login/'
                 ]


@app.before_request
def filter_path():
    """ method to check if path in excluded list or not
    """
    if auth and auth.require_auth(request.path, excluded_list):
        header = auth.authorization_header(request)
        cookie = auth.session_cookie(request)
        if not header and not cookie:
            abort(401)
        user = auth.current_user(request)
        if not user:
            abort(403)
        request.current_user = user


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ handle unauthorized error
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def not_allow(error) -> str:
    """ handle not allow access resources error
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
