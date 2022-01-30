from flask import Flask
from redis_connect.connect import RedisConnect


def create_app():
    app = Flask(__name__)
    print("App Created!")
    print("Validating DB")
    redis_connect = RedisConnect()
    if not redis_connect.is_queue_full():
        print("url queue is empty. Populating.")
        redis_connect.populate_url_queue()
    else:
        print(f"url queue is populated. Size: {redis_connect.get_queue_len()}")

    return app
