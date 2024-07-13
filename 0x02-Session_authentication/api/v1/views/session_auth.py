#!/usr/bin/env python3
"""session auth new view"""
from api.v1.views import app_views
from .users import User
from flask import request, jsonify, make_response
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def handel_routes_for_auth():
    """just for now return flask request"""
    if request.method == 'POST':
        mail = request.form.get('email')
        if not mail:
            return jsonify({ "error": "email missing" }), 401
        passwrod = request.form.get('password')
        if not passwrod:
            return jsonify({"error": "password missing"}), 400

        email = {'email': mail}
        user = User.search(email)
        if not user:
            return jsonify({ "error": "no user found for this email" })
        if user[0].is_valid_password(passwrod):
            from api.v1.app import auth
            session_id = auth.create_session(user[0].id)
            response = make_response(user[0].to_json())
            session_name = os.getenv('SESSION_NAME')
            response.set_cookie(session_name, session_id)
            return response
        else:
            return jsonify({"error": "wrong password"}), 401
