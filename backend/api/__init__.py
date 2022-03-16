from src.utility.system.log_setup.setup import default_setup, exception
from logging import getLogger, DEBUG, INFO, WARNING, ERROR, CRITICAL
from os import environ
from time import sleep

levels = {
    "debug": DEBUG,
    "info": INFO,
    "warning": WARNING,
    "error": ERROR,
    "critical": CRITICAL,
}

log_paths = ["src/logs/untimed_log.json", "src/logs/timed_log.json"]
logger = default_setup(getLogger(str(__name__)), *log_paths, level=levels["debug"])

from src.manager.mongo_manager import connectToMongo, getDb


if environ.get("PYTHON_RUN", "true").lower() == "false":
    print("Python is set to not running...")
    while True:
        print("Waiting for 20 minutes.")
        sleep(20 * 60)


connectToMongo()
dbo = getDb()