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
    print('sssssssssssssss')
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


@app.route("/sessions", methods=['DELETE', 'POST'], strict_slashes=False)
def logout() -> str:
    """
    Log out a logged in user and destroy their session
    """
    if request.method == 'DELETE':
        session_id = request.cookies.get("session_id")
        try:
            user = AUTH.get_user_from_session_id(str(session_id))
            AUTH.destroy_session(int(user.id))
            return redirect("/", code=302)
        except NoResultFound:
            abort(403)
        except InvalidRequestError:
            abort(403)



@app.route("/profile", methods=['GET'], strict_slashes=False)
def profile() -> Response:
    """check profile for the route"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    print('typeeeeeee', type(session_id))
    if not session_id:
        print('aaaaaaaaaaaaaaaaaaaaa')
        abort(403)

    try:
        user = AUTH.get_user_from_session_id(session_id)
        print('xxxxxxxxxxxxxx', user)
        if not user:
            print(f"my session id is {session_id}")
            print('bbbbbbbbbbbbbbbbbbbbbbbbbbbbb')

            abort(403)
        else:
            print('typpppppppppe', type(jsonify({"email": user.email})))
            return jsonify({"email": user.email}), 200
    except (NoResultFound, InvalidRequestError):
        print('cccccccccccccccccccccccccccccc')

        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=1)
