import logging
from logging.handlers import TimedRotatingFileHandler
from time import sleep
from os.path import dirname, abspath, exists
from os import makedirs, environ
LVL = environ.get("LOG_LEVEL", "DEBUG")

def create_path(paths):
    path = ""
    for p in paths:
        path += ("/"+p)
    return path


def logSetup(name, **kwargs):
    path = (abspath(dirname(__file__))+"/"+name)# + create_path(paths) + "/"+id
    extra ={
        "class": kwargs.get("alias", name),
        "id": f'[{kwargs.get("id", "")}]',
        "path": kwargs.get("path", ""),
    }
    if not exists(path): makedirs(path)
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(getattr(logging, LVL.upper()))
        formatter = logging.Formatter(fmt=f'%(asctime)s %(path)s %(class)-12s %(levelname)-6s %(id)-14s %(message)s',
                                        datefmt='%d-%m-%y %H:%M:%S')
        fh = TimedRotatingFileHandler(fr'{path}\{name}.log', when='midnight', interval=1, backupCount=7)
        fh.setFormatter(formatter)
        fh.namer = lambda name: name.replace(".log", "") + ".log"
        logger.addHandler(fh)
    logger = logging.LoggerAdapter(logger, extra)
    return logger