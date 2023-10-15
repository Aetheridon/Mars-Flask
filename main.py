import json

from flask import Flask
import requests

app = Flask(__name__)

@app.route("/")
def main_page():
    return "<h1>Hello Kale<h1>"

if __name__ == "__main__":
    app.run()