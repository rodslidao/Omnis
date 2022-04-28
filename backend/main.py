import threading
import time

from api import logger, dbo, CameraStreamer


try:
    from api.queries import query
    from api.mutations import mutation
    from api.subscriptions import subscription
    from src.imageStream import imgRoute, videoRoute

    from os import environ
    import uvicorn
    import socket

    from ariadne import (
        load_schema_from_path,
        make_executable_schema,
        snake_case_fallback_resolvers,
    )
    from ariadne.asgi import GraphQL

    from starlette.middleware.cors import CORSMiddleware
    from starlette.applications import Starlette
    from starlette.middleware import Middleware
    from starlette.routing import Mount

    type_defs = ""
    for _file in ["schema", "inputs", "types", "results"]:
        type_defs += load_schema_from_path(f"./src/graphql/{_file}.graphql") + (
            "\n" * 2
        )

    schema = make_executable_schema(
        type_defs, query, mutation, subscription, snake_case_fallback_resolvers
    )

    routes = [
        Mount("/imgs", routes=imgRoute),
        Mount("/videos", routes=videoRoute),
    ]

    app = Starlette(debug=True, routes=routes, on_startup=[], on_shutdown=[dbo.close])

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
    CameraStreamer.middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ]

    port = environ["SERVER_PORT"] if environ.get("SERVER_PORT") else 5000
    stream = environ["STREAMING_PORT"] if environ.get("STREAMING_PORT") else 4000
    if environ.get("ENV_MODE") == "production":
        host = "0.0.0.0"
    else:
        socketI = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socketI.connect(("8.8.8.8", 80))
        host = socketI.getsockname()[0]
        socketI.close()

    if __name__ == "__main__":
        b = threading.Thread(
            target=uvicorn.run,
            kwargs={
                "app": app,
                "host": host,
                "port": int(port),
                "log_level": logger.level,
            },
            daemon=True,
        )
        a = threading.Thread(
            target=uvicorn.run,
            kwargs={
                "app": CameraStreamer(),
                "host": host,
                "port": int(stream),
                "log_level": logger.level,
            },
            daemon=True,
        )
        a.start()
        b.start()
        while threading.active_count() > 1:
            time.sleep(1)
except Exception as e:
    dbo.close()
    CameraStreamer.shutdown()
    logger.critical(e)
