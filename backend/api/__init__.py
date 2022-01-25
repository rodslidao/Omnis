from pprint import pprint
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from pymongo import MongoClient
from os import environ

from src.exec_info import ExecutionCounter

app = Flask(__name__)
io = SocketIO(app, async_mode=None, async_handlers=True, cors_allowed_origins="*")
CORS(app)

db_port = environ.get("DB_PORT", "27017")
db_ip = environ.get("SERVER_IP", "192.168.1.30")

app.config["DATABASE_URI"] = f"mongodb://{db_ip}:{db_port}/"
db = MongoClient(app.config["DATABASE_URI"], connect=True)["Teste"]

connectedClients = 0


@app.route("/")
def hello():
    return "Home page"


@io.on("connect")
def connect():
    global connectedClients
    connectedClients += 1
    print("New Websocket Connection. Number of connected clients:", connectedClients)
    #ExecutionCounter.initialEmitAllCounts()


@io.on("disconnect")
def disconnect():
    global connectedClients
    connectedClients -= 1
    print("Client disconnected. Number of connected clients:", connectedClients)
