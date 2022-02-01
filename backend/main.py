import uvicorn
from api import dbo
# exit()
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

    # app.mount("/graphql", GraphQL(schema, debug=True))
    app = GraphQL(schema, debug=True)
    # @app.route("/graphql", methods=["GET"])
    # app.mount("/graphql", graphql_sync, schema=schema, graphiql=True)
    # def graphql_playground():
    #     logger.debug("GraphQL Playground requested")
    #     return PLAYGROUND_HTML, 200


    # @app.route("/graphql", methods=["POST", "GET"])
    # def graphql_server():
    #     data = request.get_json()
    #     success, result = graphql_sync(schema, data, context_value=request, debug=app.debug)
    #     status_code = 200 if success else 400
    #     return jsonify(result), status_code

    port = environ["SERVER_PORT"] if environ.get("SERVER_PORT") else 5000
    print("Starting server on port:", port)
    if __name__ == "__main__":
        uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")
    # io.run(app, host="0.0.0.0", port=port)

except KeyboardInterrupt:
    # io.stop()
    logger.debug("Server stopped manually")
    exit(0)
except Exception as e:
    logger.critical(e)
    exit(1)
