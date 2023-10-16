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

def get_images(user_data):
    images = []
    r = requests.get(f"https://api.nasa.gov/mars-photos/api/v1/rovers/{user_data[1]}/?api_key={user_data[0]}")
    data = r.json()
    max_sol = data["rover"]["max_sol"]
    latest_pic = False
    while not latest_pic:
        image_data_req = requests.get(f"https://api.nasa.gov/mars-photos/api/v1/rovers/{user_data[1]}/photos?sol={max_sol}&camera={user_data[2]}&api_key={user_data[0]}")
        if image_data_req.status_code != 200:
            return f"Got HTTP Error {image_data_req.status_code}"
        else:
            picture_data = image_data_req.json()
            if picture_data["photos"]:
                for pictures in picture_data["photos"]:
                    images.append(pictures["img_src"])
                latest_pic = True
            else:
                max_sol -= 1
    return images

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
        return redirect(url_for("display_images"))
    else:
        return render_template("cameras.html", cameras=cameras)

@app.route("/images", methods=["GET"])
def display_images():
    if request.method == "GET":
        image_list = get_images(user_data)
        return render_template("images.html", image_list=image_list)
    
if __name__ == "__main__":
    app.run()