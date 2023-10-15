import json

from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def main_page():
    if request.method == "POST":
        API_KEY = request.form["api"]
        print(request.form.get("Checkbox"))
        print(API_KEY)
        return render_template("index.html")
    else:   
        return render_template("index.html")

if __name__ == "__main__":
    app.run()