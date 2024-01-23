#!/usr/bin/env python3
""" module for flask app """
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
