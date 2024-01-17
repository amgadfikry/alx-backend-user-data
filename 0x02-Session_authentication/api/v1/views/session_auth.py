#!/usr/bin/env python3
""" module for session auth view """
from api.v1.views import app_views
from flask import request, jsonify, make_response
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def login_route():
    """ route mange login route
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or len(email) == 0:
        return jsonify({"error": "email missing"}), 400
    if not password or len(password) == 0:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    if not users[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(users[0].id)
    env_key = os.getenv('SESSION_NAME')
    res = make_response(jsonify(users[0].to_json()))
    res.set_cookie(env_key, session_id)
    return res
