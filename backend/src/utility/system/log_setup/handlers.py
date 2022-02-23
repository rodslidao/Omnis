from logging.handlers import TimedRotatingFileHandler
from logging import StreamHandler, FileHandler
from time import gmtime




def handlers_factory(handler):
    def wrapper(level, formatter, destination):
            h = handler(destination)
            h.setLevel(level)
            h.formatter = formatter
            h.formatter.converter = gmtime
            h.namer = lambda name: name.replace(".json", "") + ".json"
            return h
    return wrapper

@handlers_factory
def stream_handler(destination):
    return StreamHandler(destination)

@handlers_factory
def file_handler(destination):
    return FileHandler(destination)

@handlers_factory
def time_file_handler(destination):
    return TimedRotatingFileHandler(destination, when='midnight', interval=1, backupCount=7)

handlers = {
    "stream": stream_handler,
    "file": file_handler,
    "time_file": time_file_handler,
}