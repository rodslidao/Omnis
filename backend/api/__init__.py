from src.utility.system.log_setup.setup import default_setup, exception
from logging import getLogger, DEBUG, INFO, WARNING, ERROR, CRITICAL

levels = {
    "debug": DEBUG,
    "info": INFO,
    "warning": WARNING,
    "error": ERROR,
    "critical": CRITICAL,
}

log_paths = ["src/logs/untimed_log.json", "src/logs/timed_log.json"]
logger = default_setup(getLogger(__name__), *log_paths, level=levels["debug"])
"""
from src.manager.mongo_manager import connectToMongo, getDb

from os import environ
from time import sleep

if environ.get("PYTHON_RUN", "true").lower() == "false":
    print("Python is not running...")
    while True:
        print("Waiting for 20 minutes...")
        sleep(20 * 60)


connectToMongo()
dbo = getDb()

# connect_to_socketio()
# io = get_io()
# app = get_app()
"""