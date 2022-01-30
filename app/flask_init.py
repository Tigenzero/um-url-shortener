from flask import Flask
from string import ascii_lowercase, ascii_uppercase
from itertools import combinations
from redis_connect.connect import RedisConnect
from collections import deque
from random import choice


def populate_url_queue(redis_connect: RedisConnect):
    url_len = redis_connect.get_next_url_len()
    if url_len is None:
        url_len = 3
    queue = deque()
    for key in combinations(f"{ascii_lowercase}{ascii_uppercase}{''.join([str(x) for x in range(10)])}", url_len):
        url = "".join(key)
        if choice([0, 1]):
            queue.append(url)
        else:
            queue.appendleft(url)
    redis_connect.queue_tiny_urls(queue, url_len)
    print(redis_connect.get_queue_len())


def create_app():
    app = Flask(__name__)
    print("App Created!")
    print("Validating DB")
    redis_connect = RedisConnect()
    if not redis_connect.is_queue_full():
        print("url queue is empty. Populating.")
        populate_url_queue(redis_connect)
    else:
        print(f"url queue is populated. Size: {redis_connect.get_queue_len()}")

    return app
