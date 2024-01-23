#!/usr/bin/env python3
""" module for flask app """
from flask import (Flask, jsonify, request, abort, make_response,
                   redirect, url_for)
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def main_route():
    """ route to main
    """
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    """ route to check if email is register or create new user
    """
    email, password = request.form.values()
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ login route to create session_id and sent with cookies
    """
    email, password = request.form.values()
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        res = make_response(
                jsonify({"email": email, "message": "logged in"}))
        res.set_cookie('session_id', session_id)
        return res
    abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ route that remove session_id
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for('main_route'))
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
