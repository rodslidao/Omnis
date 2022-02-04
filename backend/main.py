from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import JSONResponse
import uvicorn
from api import *
from src.imageStream import imgRoute, videoRoute
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from src.logs.log import logSetup
logger = logSetup("Api")
try:

    # from api import app, io
    from sys import exit
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

    type_defs = load_schema_from_path("schema.graphql")
    schema = make_executable_schema(
        type_defs, query, mutation, subscription, snake_case_fallback_resolvers
    )

    middleware = [
        Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
    ]

    async def user(request):
        print(request.path_params["username"])
        return JSONResponse({"hello": "world"})

    routes = [
        Route("/", GraphQL(schema, middleware=middleware)),
        Mount('/imgs', routes=imgRoute),
        Mount('/videos', routes=videoRoute),
    ]

    app = Starlette(debug=True, middleware=middleware, routes=routes)
    # app.mount("/", GraphQL(schema, debug=True))


    port = environ["SERVER_PORT"] if environ.get("SERVER_PORT") else 5000
    if __name__ == "__main__":
        uvicorn.run("main:app", host="192.168.1.30", port=int(port), log_level="info")

except KeyboardInterrupt:
    logger.debug("Server stopped manually")
    exit(0)
except Exception as e:
    logger.critical(e)
    exit(1)
