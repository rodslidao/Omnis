import uvicorn
from api import dbo
from starlette.middleware.cors import CORSMiddleware
from src.logs.log import logSetup
logger = logSetup("Api")
try:

    # from api import app, io
    from sys import exit
    from ariadne import (
        load_schema_from_path,
        make_executable_schema,
        graphql_sync,
        snake_case_fallback_resolvers,
    )
    from ariadne.constants import PLAYGROUND_HTML
    from flask import request, jsonify
    from api.queries import query
    from api.mutations import mutation
    from api.subscriptions import subscription
    from os import environ
    from ariadne.asgi import GraphQL

    type_defs = load_schema_from_path("schema.graphql")
    schema = make_executable_schema(
        type_defs, query, mutation, subscription, snake_case_fallback_resolvers
    )

    app = CORSMiddleware(GraphQL(schema, debug=True), allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])


    port = environ["SERVER_PORT"] if environ.get("SERVER_PORT") else 5000
    print("Starting server on port:", port)
    if __name__ == "__main__":
        uvicorn.run("main:app", host="0.0.0.0", port=int(port), log_level="info")

except KeyboardInterrupt:
    logger.debug("Server stopped manually")
    exit(0)
except Exception as e:
    logger.critical(e)
    exit(1)
