from starlette.applications import Starlette
from starlette.routing import Route, Mount
import uvicorn
from api import *
from src.imageStream import imgRoute, videoRoute
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from src.logs.log import logSetup
import socket
logger = logSetup("Api")

try:

    from ariadne import (
        load_schema_from_path,
        make_executable_schema,
        snake_case_fallback_resolvers,
    )


    from api.queries import query
    from api.mutations import mutation
    from api.subscriptions import subscription
    from os import environ
    from ariadne.asgi import GraphQL

    type_defs = ""
    for _file in ["schema", "inputs", "types", "results"]:
        type_defs += load_schema_from_path(f"./src/graphql/{_file}.graphql")+('\n'*2)

    schema = make_executable_schema(
        type_defs, query, mutation, subscription, snake_case_fallback_resolvers
    )

    middleware = [
        Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
    ]


    routes = [
        Mount('/imgs', routes=imgRoute),
        Mount('/videos', routes=videoRoute),
    ]

    app = Starlette(debug=True, routes=routes)
    ls = CORSMiddleware(GraphQL(schema, debug=True), allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])


    app.mount("/", ls)


    port = environ["SERVER_PORT"] if environ.get("SERVER_PORT") else 5000
    if environ.get("ENV_MODE") == "production":
        host = "0.0.0.0"
    else:
        socketI = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socketI.connect(("8.8.8.8", 80))
        host = socketI.getsockname()[0]
        socketI.close()

    if __name__ == "__main__":
        uvicorn.run("main:app", host=host, port=int(port), log_level="info")

except KeyboardInterrupt:
    logger.debug("Server stopped manually")
    exit(0)
except Exception as e:
    logger.critical(e)
    print(e)
    exit(1)
