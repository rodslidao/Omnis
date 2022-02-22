from operator import le
from coloredlogs import install
from src.utility.system.log_setup.handlers import handlers
from src.utility.system.log_setup.decorators import exception
from src.utility.system.log_setup.formatters import formatters
from logging import DEBUG
install(microseconds=True)

def custom_handler(logger, handler_name, formatter_name, destination, level):
    handler = handlers[handler_name](level, formatters[formatter_name], destination)
    logger.addHandler(handler)

def default_setup(logger, logfilepath, timedlogfilepath, level=DEBUG):
    logger.setLevel(level)
    custom_handler(logger, "file", "json", logfilepath, level)
    custom_handler(logger,"time_file", "json", timedlogfilepath, level)
    # custom_handler(logger,"time_file", "json", nodelogfilepath, level)
    return logger