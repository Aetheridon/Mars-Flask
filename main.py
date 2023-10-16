import json

from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
user_data = [] # 0 is API key, 1 is the Rover, 2 is the camera

def get_rover_data(user_data):
    rover_cameras = []
    r = requests.get(f"https://api.nasa.gov/mars-photos/api/v1/rovers/{user_data[1]}/?api_key={user_data[0]}")
    rover_data = r.json()
    for camera in rover_data["rover"]["cameras"]:
        rover_cameras.append(camera["name"])
    return rover_cameras

@app.route("/", methods=["POST", "GET"])
def main_page():
    if request.method == "POST":
        API_KEY = request.form["api"]
        rover = request.form.get("Checkbox")
        user_data.append(API_KEY)
        user_data.append(rover)
        return redirect(url_for("camera_selector"))
    else:   
        return render_template("index.html")
    
@app.route("/cameras", methods=["POST", "GET"])
def camera_selector():
    cameras = get_rover_data(user_data)
    if request.method == "POST":
        user_data.append(request.form.get("selected-camera"))
        return f"<h1>{user_data}</h1>"
    else:
        return render_template("cameras.html", cameras=cameras)

if __name__ == "__main__":
    app.run()