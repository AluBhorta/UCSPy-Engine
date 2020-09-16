import json
import time

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit

from core.models.UCSPyEngine import UCSPyEngine

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

started = False


def send_progress(data={"name": "wow"}):
    socketio.emit("progress", json.dumps(data))


@socketio.on('solve')
def handle_solve(solverT):
    r = json.loads(solverT)
    print(f"Solver started! {r}")

    # UCSPyEngine().solve()
    started = True

    while started:
        emit("progress", {
            "id": "string",
            "epoch": "string",
            "fitness": "21",
        })
        time.sleep(5)


@socketio.on('stop')
def handle_stop(id):
    print("stopped", id)
    started = False
