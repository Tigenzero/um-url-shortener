import os
from collections import deque
from itertools import combinations
import random
from string import ascii_lowercase, ascii_uppercase
from redis import Redis
from redis_connect.singleton import Singleton

REDIS_SERVER = os.getenv("REDIS_SERVER")
REDIS_PORT = os.getenv("REDIS_PORT")
QUEUE = "queue:url"
NEXT_URL_LEN = "queue:url_len"
URL_DESIGNATION = "key"
KEY_CHARS = f"{ascii_lowercase}{ascii_uppercase}{''.join([str(x) for x in range(10)])}"


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
        # This would be a background check with celery to refill if the queue got too low
        if not self.is_queue_full():
            self.populate_url_queue()
        return self.connect.rpop(QUEUE).decode("utf-8")

    def queue_tiny_urls(self, url_list, url_len):
        self.connect.set(NEXT_URL_LEN, url_len + 1)
        self.connect.lpush(QUEUE, *url_list)

    def store_url(self, url):
        tiny_url = self.get_tiny_url()
        self._store_url(f"{URL_DESIGNATION}:{tiny_url}", url)
        return tiny_url

    def _store_url(self, key, url):
        self.connect.set(key, url)

    def get(self, key):
        tiny_key = f"{URL_DESIGNATION}:{key}"
        if self.connect.exists(tiny_key):
            return self.connect.get(tiny_key).decode("utf-8")

    def delete(self, keys):
        # to only be used in testing
        self.connect.delete(keys)

    def populate_url_queue(self):
        url_len = self.get_next_url_len()
        if url_len is None:
            url_len = 4
        queue = deque()
        for key in combinations(KEY_CHARS, url_len):
            url = "".join(key)
            if random.choice([0, 1]):
                queue.append(url)
            else:
                queue.appendleft(url)
        self.queue_tiny_urls(queue, url_len)
        print(self.get_queue_len())
