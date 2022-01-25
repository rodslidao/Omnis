if __package__ is None:
    import sys
    from os import path

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.loader import loadConfig, LodingMode

# from nodes.node_manager import NodeManager
from src.manager.mongo_manager import getDb, connectToServer
from src.exec_info import ExecutionCounter
import os

from flask_socketio import (
    SocketIO,
)

from flask import Flask, Response, request

from flask_cors import CORS
from bson.objectid import ObjectId

port = os.environ.get("PORT", "5000")
host = os.environ.get("HOST", "192.168.1.41")

io = None
app = None
dbo = None


connectedClients = 0


def call():
    global io, app, dbo
    dbo = getDb()
    loadConfig(dbo, LodingMode.STARTUP)
    app = Flask(__name__)
    io = SocketIO(app, async_mode=None, async_handlers=True, cors_allowed_origins="*")
    CORS(app)

    @io.on("connect")
    def connect():
        global connectedClients
        connectedClients += 1
        print(
            "New Websocket Connection. Number of connected clients:", connectedClients
        )

        ExecutionCounter.initialEmitAllCounts()

        @io.on("disconnect")
        def disconnect():
            global connectedClients
            connectedClients -= 1
            print("Client disconnected. Number of connected clients:", connectedClients)


connectToServer(call)


@app.route("/node-config/<id>", methods=["GET"])
def getNodeConfig(id):
    query = {"_id": ObjectId(id)}
    data = dbo.get_collection("node-configs").find_one(query)
    io.emit("INDEX-RESPONSE", data)
    return Response(data)


@app.route("/node-config/all", methods=["GET"])
def getAllNodeConfigs():
    data = dbo.get_collection("node-configs").find()
    io.emit("INDEX-RESPONSE", data)
    return Response(data)


@app.route("/node-config/<id>", methods=["DELETE"])
def deleteNodeConfig(id):
    query = {"_id": ObjectId(id)}
    obj = dbo.get_collection("node-configs").delete_one(query)
    io.emit("INDEX-RESPONSE", {"num_deleted": obj["result"]["n"]})
    return Response("")


@app.route("/node-config/<id>", methods=["POST"])
def updateNodeConfig(id):
    query = {"_id": ObjectId(id)}
    obj = dbo.get_collection("node-configs").update_one(query, request.json)
    io.emit("INDEX-RESPONSE", {"num_updated": obj["result"]["n"]})
    return Response("")


# io.run(app, host=host, port=port)
# connectToServer(call)
