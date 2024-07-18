#!/usr/bin/env python3
"""app flask point"""
import flask
from flask import Flask, jsonify, request, abort, Response
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

app = Flask(__name__)
auth = Auth()


@app.route("/", methods=['GET'])
def index():
    """start point of flask"""
    payload = {"message": "Bienvenue"}
    return jsonify(payload)


@app.route("/users", methods=['POST'], strict_slashes=False)
def users():
    """create user if email doesn't exist"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            user = auth.register_user(email, password)
            paylod = {"email": email, "message": "user created"}
            return jsonify(paylod)
        except ValueError:
            return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> Response:
    """login function"""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            x = auth.valid_login(email, password)
            if not x:
                abort(401)
            session_id = auth.create_session(email)
            response = jsonify({"email": email, "message": "logged in"}), 200
            response.set_cookie("session_id", session_id)
            return response
        except NoResultFound:
            abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=1)
