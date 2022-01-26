from api import app, io, loadConfig, LoadingMode, dbo
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
from os import environ

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value=request, debug=app.debug)
    status_code = 200 if success else 400
    return jsonify(result), status_code


port = environ["SERVER_PORT"] if environ.get("SERVER_PORT") else 5000
io.run(app, host="0.0.0.0", port=port)
