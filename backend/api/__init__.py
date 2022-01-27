from src.manager.mongo_manager import connectToMongo, getDb
from src.manager.socketio_manager import connect_to_socketio, get_io, get_app
from src.loader import loadConfig, LoadingMode
import sys, os, logging
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def blockLogging():
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

if os.environ.get("BLOCK_PRINT"):
    blockPrint()

if os.environ.get("BLOCK_LOGGING"):
    blockLogging()
    
connectToMongo()
dbo = getDb()
#loadConfig(dbo, LoadingMode.STARTUP)

connect_to_socketio()
io = get_io()
app = get_app()


# Disable