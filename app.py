import io
import os
import requests
import json
import pyheif

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from PIL import Image

# Function to convert HEIC to JPEG
def convert_heic_to_jpg(file_stream):
    heif_file = pyheif.read(file_stream) # read HEIC file from stream
    # convert to PIL Image
    image = Image.frombytes(
        heif_file.mode, heif_file.size, heif_file.data, "raw", heif_file.mode, heif_file.stride
    )
    jpg_stream = io.BytesIO() # create a BytesIO stream to hold the JPEG data
    image.save(jpg_stream, format="JPEG") # save the image as JPEG into in-memory stream
    jpg_stream.seek(0) # reset pointer to start at the beginning of stream
    return jpg_stream # returns the in-memory JPEG stream

# creates the Flask application and initializes the session
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

load_dotenv()  # Reads from .env file
API_KEY = os.getenv("PLANT_ID_API_KEY")   # get API key from environment variable
PROJECT = "all" # define project type
api_endpoint = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={API_KEY}"

# Route for the home page
@app.route("/")
def index():
    return render_template("index.html")

# Route for the new identification page
@app.route("/newID", methods=["GET", "POST"])
def newID():
    if request.method == "POST":
        # check if image file is present
        if "weed_image" not in request.files:
            flash("No file uploaded.")
            return redirect("/newID")

        file = request.files["weed_image"] # get the uploaded file

        # check if file is valid
        if file.filename == "":
            flash("No file selected.")
            return redirect("/newID")
        
        data = {"organs": ["auto"]} # let API AI decide organ uploaded

        # check if file is HEIC or HEIF
        if file.filename.lower().endswith(".heic") or file.mimetype.startswith("image/hei"):
            converted = convert_heic_to_jpg(file.stream) # convert stream to JPEG
            filename_jpg = file.filename.rsplit('.', 1)[0] + ".jpg" # convert filename to JPEG
            # create a tuple for the converted file
            files = [
                ("images", (filename_jpg, converted, "image/jpeg"))
            ]
        else:
            files = [
                ("images", (file.filename, file.stream, file.content_type))
            ]

        req = requests.Request("POST", url=api_endpoint, files=files, data=data) # create a request object
        prepared = req.prepare() # prepare the request

        session = requests.Session() # create a session
        response = session.send(prepared) # send the request
        # check if the response is successful and returns identification results
        if response.status_code == 200:
            data = response.json()
            return render_template("results.html", data=data)
        # flash an error message if the response is not successful
        else:
            flash("Error occurred while processing the image.")
            return redirect("/newID")
        
    else:
        return render_template("newID.html")

# Route for the about page
@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True) # , host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

