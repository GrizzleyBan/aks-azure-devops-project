import os
import socket

import redis
from flask import Flask, jsonify

app = Flask(__name__)
cache = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379, decode_responses=True)


@app.route("/api/visits")
def visits():
    count = cache.incr("visits")
    return jsonify(visits=count, served_by=socket.gethostname())


@app.route("/health")
def health():
    return jsonify(status="ok")