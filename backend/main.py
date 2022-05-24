from os import environ
import threading
import uvicorn
import socket
import time

from api import logger, dbo, stremer
from api.queries import query
from api.subscriptions import subscription
from api.mutations import mutation

from src.nodes.node_registry import NodeRegistry
from src.end_points import imgRoute, videoRoute, custom_video_response, frame_producer
from src.nodes.node_manager import NodeManager
from src.loader import extractOptionsFromNode
from src.manager.camera_manager import CameraManager

from starlette.routing import Route

from ariadne.asgi import GraphQL
from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    snake_case_fallback_resolvers,
)

from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Mount, WebSocketRoute
from starlette.endpoints import WebSocketEndpoint
from starlette.applications import Starlette
from starlette.middleware import Middleware


type_defs = ""
for _file in ["schema", "inputs", "types", "results"]:
    type_defs += load_schema_from_path(f"./src/graphql/{_file}.graphql") + ("\n" * 2)


schema = make_executable_schema(
    type_defs, query, mutation, subscription, snake_case_fallback_resolvers
)


class Echo(WebSocketEndpoint):
    encoding = "json"
    _id = None

    async def on_connect(self, websocket):
        await websocket.accept()

    async def on_receive(self, websocket, data):
        node_id = data.get("nodeId")
        if node_id:
            node_type = data.get("nodeType")
            running_node = NodeManager.getNodeById(node_id)
            if running_node:
                running_node.update_options(extractOptionsFromNode(data))
        await websocket.send_json({"a": "b"})
    async def on_disconnect(self, websocket, close_code=100):
        print("disconnected")


routes_app = [
    Mount("/imgs", routes=imgRoute),
    WebSocketRoute("/ws", endpoint=Echo),
]

stremer.routes.append(Route("/videos/{video_id}", endpoint=custom_video_response, methods=["GET", "POST"]))
stremer.config["generator"] = frame_producer

app = Starlette(debug=True, routes=routes_app, on_startup=[], on_shutdown=[dbo.close])

app.mount(
    "/",
    CORSMiddleware(
        GraphQL(schema, debug=True),
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    "Omnis",
)

stremer.middleware = [
    Middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
]


port = environ["SERVER_PORT"] if environ.get("SERVER_PORT") else 5000
stream = environ["STREAMING_PORT"] if environ.get("STREAMING_PORT") else 4000
if environ.get("ENV_MODE") == "production":
    host = "0.0.0.0"
elif environ.get("SERVER_IP"):
    host = environ["SERVER_IP"]
else:
    socketI = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socketI.connect(("8.8.8.8", 80))
    host = socketI.getsockname()[0]
    socketI.close()

if __name__ == "__main__":
    app_server = threading.Thread(
        target=uvicorn.run,
        kwargs={
            "app": app,
            "host": host,
            "port": int(port),
            "log_level": logger.level,
        },
        daemon=True,
    )
    image_stream_server = threading.Thread(
        target=uvicorn.run,
        kwargs={
            "app": stremer(),
            "host": host,
            "port": int(stream),
            "log_level": logger.level,
        },
        daemon=True,
    )
    app_server.start()
    image_stream_server.start()
    try:
        while threading.active_count() > 1:
            time.sleep(1)
    except KeyboardInterrupt:
        CameraManager.stop()
        stremer.shutdown()
        image_stream_server.join(2)
    finally:
        app_server.join(1)
        dbo.close()
