if __package__ is None:
    import sys
    from os import path

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import redis
import os

url = "redis://redis:6379/0"
environment = os.environ.get("NODE_ENV", "DEV")
if environment == "DEV":
    url = "redis://localhost:6379/0"

client = redis.Redis.from_url(url)


def getAsync(key):
    return client.get(key)


class RedisClient:
    def set(key, value):
        client.set(key, value)

    def incrby(key, value):
        client.incrby(key, value)

    def get(key):
        return getAsync(key)
