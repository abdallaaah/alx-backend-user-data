#!/usr/bin/env python3
"""app flask point"""
from auth import Auth
import flask
from flask import Flask, jsonify, request, abort, Response, url_for, redirect
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

app = Flask(__name__)
AUTH = Auth()


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
            user = AUTH.register_user(email, password)
            paylod = {"email": email, "message": "user created"}
            return jsonify(paylod)
        except ValueError:
            return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login() -> str:
    """Log in a user and create a session """
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            if AUTH.valid_login(email, password):
                pass
            else:
                abort(401)
            session_id = AUTH.create_session(email)
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie("session_id", session_id)
            return response, 200
        except NoResultFound:
            abort(401)

        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response, 200


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """
    Log out a logged in user and destroy their session
    """
    session_id = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(str(session_id))
    if user is None or session_id is None:
        abort(403)
    AUTH.destroy_session(int(user.id))
    return redirect('/'), 302


@app.route("/profile", methods=['GET'], strict_slashes=False)
def profile() -> Response:
    """check profile for the route"""
    session_id = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None or session_id is None:
        abort(403)
    return jsonify({"email": f"{user.email}"}), 200


@app.route("/reset_password ", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """if user regiester return rest password token"""
    email = request.form.get("email")
    try:
        token = auth.get_reset_password_token(email)
        if not token:
            abort(403)
        return jsonify({"email": f"{email}", "reset_token": f"{token}"}), 200
    except ValueError:
        abort(403)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=1)
