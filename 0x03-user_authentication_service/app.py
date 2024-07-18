#!/usr/bin/env python3
"""app flask point"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    """start point of flask"""
    payload = {"message": "Bienvenue"}
    return jsonify(payload)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=1)
