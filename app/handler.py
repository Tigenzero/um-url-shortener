from flask import request, render_template
from app import flask_init
from app.url_func import get_big_url, get_request_url
from redis_connect.connect import RedisConnect

app = flask_init.create_app()


@app.route("/")
def launch_page():
    return render_template('get_url.html')


@app.route("/<url_key>", methods=["GET"])
def get_url(url_key):
    redis_connect = RedisConnect()
    url = get_big_url(url_key, redis_connect)
    if url is None:
        return render_template('404.html'), 404
    return url


@app.route("/<big_url>", methods=["POST"])
def post_url(big_url):
    redis_connect = RedisConnect()
    return redis_connect.store_url(big_url)


@app.route("/send_url", methods=["POST"])
def convert_url_from_form():
    # big_url = get_request_url(request)
    big_url = request.form["big_url"]
    if big_url is None:
        big_url = request.get_json(force=True).get("url")
        if big_url is None:
            return render_template('404.html'), 404
    redis_connect = RedisConnect()
    return redis_connect.store_url(big_url)


@app.route("/send_url_json", methods=["POST"])
def convert_url_from_json():
    big_url = request.get_json(force=True).get("url")
    if big_url is None:
        return render_template('404.html'), 404
    redis_connect = RedisConnect()
    return redis_connect.store_url(big_url)
