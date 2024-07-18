#!/usr/bin/env python3
"""app flask point"""
from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
auth = Auth()


@app.route("/", methods=['GET'])
def index():
    """start point of flask"""
    payload = {"message": "Bienvenue"}
    return jsonify(payload)


@app.route("/users", methods=['POST'], strict_slashes=False)
def users():
    """"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form['password']

        try:
            paylod = {"email": f"{email}", "message": "user created"}
            return jsonify(paylod)
        except ValueError:
            user = auth.register_user(email, password)
            if user:
                return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=1)
