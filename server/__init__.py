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


@socketio.on('connect')
def handle_connect():
    #     connected = True
    print('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


@socketio.on('message')
def handle_message(message):
    print(f'received message: {message}')
    send('ping!')


def send_progress(data={"name": "wow"}):
    socketio.emit("progress", json.dumps(data))


@socketio.on('solve')
def handle_solve(config):
    r = json.loads(config)
    print(r)

    # start new solver
    UCSPyEngine().solve()

    started = True
    # send_progress()


@socketio.on('stop')
def handle_stop(id):
    print("stopped", id)
    started = False
    send(f"STOPPED! {id}")
