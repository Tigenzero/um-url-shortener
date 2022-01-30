from flask import Flask


def create_app():
    app = Flask(__name__)
    print("App Created!")
    return app