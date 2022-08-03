from api import dbo
from ariadne import ScalarType
from bson import ObjectId
from bson.dbref import DBRef

ID = ScalarType("ID")
DB_VALUE = ScalarType("DB_VALUE")

DBREF_object = ScalarType("DBREF_object")
DBREF_matrix = ScalarType("DBREF_matrix")
DBREF_process = ScalarType("DBREF_process")
DBREF_variable = ScalarType("DBREF_variable")
DBREF_sketch = ScalarType("DBREF_sketch")

@ID.serializer
def ID_serializar(value):
    if isinstance(value, ObjectId): return str(value)
    elif isinstance(value, dict):
        for k, v in value.items():
           value[k] = ID_serializar(v)
        return value
    elif isinstance(value, list):
        return list(map(ID_serializar, value))
    return value


@ID.value_parser
def ID_v_parser(value):
    if value:
        return ObjectId(value)
    return value

@ID.literal_parser
def ID_l_parser(ast):
    return ID_v_parser(str(ast.value))


@DB_VALUE.serializer
def DB_VALUE_serializar(value, collection=None):
    if isinstance(value, DBRef):
        return ID_serializar(dbo.find_one(value.collection, {'_id':value.id}))
    elif not isinstance(value, str):
        if isinstance(value.get("_id"), ObjectId) and value.get("collection", collection):
            return ID_serializar(dbo.find_one(value.get("collection", collection), {"_id":value["_id"]}))
    return value

@DB_VALUE.value_parser
def DB_VALUE_v_parser(value, collection=None):
    if isinstance(value, dict):
        return {"$ref":value.get('ref', collection), '$id': ID_v_parser(value['_id'])}
    elif isinstance(value, list):
        if not collection:
            return list(map(DB_VALUE_v_parser, value))
        else:
            return [DB_VALUE_v_parser(v,collection) for v in value]

@DBREF_object.value_parser
def DBREF_object_v_parser(value):
    return DB_VALUE_v_parser(value, collection='object')

@DBREF_matrix.value_parser
def DBREF_matrix_v_parser(value):
    return DB_VALUE_v_parser(value, collection='matrix')

@DBREF_process.value_parser
def DBREF_process_v_parser(value):
    return DB_VALUE_v_parser(value, collection='process')

@DBREF_variable.value_parser
def DBREF_variable_v_parser(value):
    return DB_VALUE_v_parser(value, collection='variable')

@DBREF_sketch.value_parser
def DBREF_sketch_v_parser(value):
    return DB_VALUE_v_parser(value, collection='sketch')

custom_types = [ID, DB_VALUE, DBREF_object, DBREF_matrix, DBREF_process, DBREF_variable, DBREF_sketch]
