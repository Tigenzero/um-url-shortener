import os
from redis import Redis
from redis_connect.singleton import Singleton

REDIS_SERVER = os.getenv("REDIS_SERVER")
REDIS_PORT = os.getenv("REDIS_PORT")
QUEUE = "queue:url"
NEXT_URL_LEN = "queue:url_len"


class RedisConnect(metaclass=Singleton):
    def __init__(self, db=0):
        self.connect = Redis(host=REDIS_SERVER, port=REDIS_PORT, db=db)

    def is_queue_full(self):
        return self.connect.llen(QUEUE) != 0

    def get_queue_len(self):
        return self.connect.llen(QUEUE)

    def get_next_url_len(self):
        if self.connect.exists(NEXT_URL_LEN):
            return self.connect.get(NEXT_URL_LEN)

    def get_tiny_url(self):
        if self.is_queue_full():
            return self.connect.rpop(QUEUE).decode("utf-8")

    def queue_tiny_urls(self, url_list, url_len):
        self.connect.set(NEXT_URL_LEN, url_len + 1)
        self.connect.lpush(QUEUE, *url_list)

    def push(self, key, url):
        self.connect.set(key, url)

    def get(self, key):
        if self.connect.exists(key):
            return self.connect.get(key).decode("utf-8")

    def delete(self, keys):
        # to only be used in testing
        self.connect.delete(keys)
