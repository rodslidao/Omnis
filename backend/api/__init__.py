from src.manager.mongo_manager import connectToMongo, getDb
from src.manager.socketio_manager import connect_to_socketio, get_io, get_app
from src.loader import loadConfig, LoadingMode

    
connectToMongo()
dbo = getDb()
#loadConfig(dbo, LoadingMode.STARTUP)

connect_to_socketio()
io = get_io()
app = get_app()