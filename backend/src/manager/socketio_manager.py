# from flask import Flask
# from flask_cors import CORS
# from flask_socketio import SocketIO

from starlette.applications import Starlette

from bson import ObjectId

io = None
app = None


def connect_to_socketio():
    global io, app

    if app is None:
        # app = Flask(__name__)
        app = Starlette(debug=True)
        # CORS(app)

    # if io is None:
    #     #io = SocketIO(app, cors_allowed_origins="*", cors_allowed_headers="*", cors_allowed_methods="*")

    # #io.emit("connected", {"data": "connected"})
    # @app.route("/")
    # def hello():
    #     #io.emit("server", {"data": "connected"})
    #     return "Home page"

    # @io.on("connect")
    # def connect():
    #     _id = ObjectId()
    #     print(f"New Client [{_id}]")
    #     #global connectedClients
    #     #connectedClients += 1
    #     #print("New Websocket Connection. Number of connected clients:", connectedClients)
    #     #ExecutionCounter.initialEmitAllCounts()

    #     @io.on("disconnect")
    #     def disconnect():
    #         print(f"Client [{_id}] disconnected")
    #         #global connectedClients
    #         #connectedClients -= 1
    #         #print("Client disconnected. Number of connected clients:", connectedClients)


def get_io():
    return io


def emit(event, payload):
    # get_io().emit(event, payload)
    pass


def get_app():
    return app
