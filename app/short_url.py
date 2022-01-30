from flask import request
from u_masters.app import flask_init


app = flask_init.create_app()


@app.route("/", methods=["POST", "GET"])
def begin():
    return f"oh hi there {request.method}"
