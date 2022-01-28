from re import S
from src.manager.mongo_manager import connectToMongo, getDb
from src.manager.socketio_manager import connect_to_socketio, get_io, get_app
from os import environ
from time import sleep
if not environ.get("PYTHON_RUN", True):
    while True:
        print("a")
        sleep(3600)
        



connectToMongo()
dbo = getDb()

connect_to_socketio()
io = get_io()
app = get_app()
