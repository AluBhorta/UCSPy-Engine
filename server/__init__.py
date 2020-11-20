import json
import time

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit
from concurrent import futures

from core.models.UCSPyEngine import UCSPyEngine

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# engine = UCSPyEngine()
executor = futures.ProcessPoolExecutor()

# import multiprocessing as mp
# pool = mp.Pool()


""" mock impl """


def mock_solve(sleepForSecs=10, solver=None):
    print(f"mocking 'solve' for {sleepForSecs}s...")
    # send_started(solver)

    time.sleep(sleepForSecs)

    print("ending mock solve...")
    # send_completed(solver)


def mock_stop(sleepForSecs=5, solver=None):
    print(f"mocking 'stop' for {sleepForSecs}s...")

    time.sleep(sleepForSecs)

    print("ending mock stop...")
    # send_stopped(solver)


""" event listeners """


@socketio.on('get:solvers')
def receive_get_solvers():
    # send/paginate the metadata of solvers from db
    pass


@socketio.on('solve')
def receive_solve(solver):
    print("got 'solve'")
    solver = json.loads(solver)

    send_started(solver)

    f = executor.submit(mock_solve, 10, solver)
    res = f.result()

    send_completed(solver)

    return {"msg": "received 'solve'!"}


@socketio.on('stop')
def receive_stop(solver):
    print("got 'stop'")
    solver = json.loads(solver)

    executor.submit(mock_stop, 5, solver)

    send_stopped(solver)

    return {"msg": "received 'stop'!"}


@socketio.on('plot')
def receive_plot(arg):
    print("got 'plot'")
    print("arg: ", arg)
    return {"msg": "received 'plot'!"}


@socketio.on('inspect')
def receive_inspect(arg):
    print("got 'inspect'")
    print("arg: ", arg)
    return {"msg": "received 'inspect'!"}


""" event senders """


def send_started(solver):
    print("sending started...")
    emit("started", solver)


def send_completed(solver):
    print("sending completed...")
    emit("completed", solver)


def send_stopped(solver):
    print("sending stopped...")
    emit("stopped", solver)


def send_failed(solver):
    print("sending failed...")
    emit("failed", solver)


def send_progress():
    pass


""" others """


def cleanup():
    executor.shutdown(wait=True)
    print("done cleanup :)")
