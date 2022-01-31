from src.manager.mongo_manager import connectToMongo, getDb
from src.manager.socketio_manager import connect_to_socketio, get_io, get_app
from os import environ
from time import sleep

if environ.get("PYTHON_RUN", "true").lower() == "false":
    print("Python is not running...")
    while True:
        print("Waiting for 20 minutes...")
        sleep(20*60)


connectToMongo()
dbo = getDb()

connect_to_socketio()
io = get_io()
app = get_app()
