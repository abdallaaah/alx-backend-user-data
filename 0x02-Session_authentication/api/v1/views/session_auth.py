#!/usr/bin/env python3
"""session auth new view"""
from api.v1.views import app_views
from .users import User
from flask import request, jsonify, make_response
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session():
    """just for now return flask requesttt"""
    if request.method == 'POST':
        mail = request.form.get('email')
        if not mail:
            return jsonify({"error": "email missing"}), 401
        passwrod = request.form.get('password')
        if not passwrod:
            return jsonify({"error": "password missing"}), 400

        email = {'email': mail}
        users = User.search(email)
        if not users or users == []:
            return jsonify({"error": "no user found for this email"}), 404
        for user in users:
            if user.is_valid_password(passwrod):
                from api.v1.app import auth
                session_id = auth.create_session(user.id)
                response = make_response(user.to_json())
                session_name = os.getenv('SESSION_NAME')
                response.set_cookie(session_name, session_id)
                return response
            else:
                return jsonify({"error": "wrong password"}), 401


@app_views.route('auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def delete():
    from api.v1.app import auth
    x = auth.destroy_session(request)
    if x == 'False':
        abort(404)
    return jsonify({}), 200
