import io
import os
import requests
import json
import pyheif

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from pprint import pprint
from PIL import Image

# Function to convert HEIC to JPEG
def convert_heic_to_jpg(file_stream):
    # read HEIC file from stream
    heif_file = pyheif.read(file_stream)
    # convert to PIL Image
    image = Image.frombytes(
        heif_file.mode, heif_file.size, heif_file.data, "raw", heif_file.mode, heif_file.stride
    )
    jpg_stream = io.BytesIO()
    image.save(jpg_stream, format="JPEG")
    jpg_stream.seek(0)
    return jpg_stream

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

load_dotenv()  # Reads from .env file
API_KEY = os.getenv("PLANT_ID_API_KEY")   # Your API key here
PROJECT = "all" # You can choose a more specific flora, see: /docs/newfloras
api_endpoint = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={API_KEY}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/newID", methods=["GET", "POST"])
def newID():
    if request.method == "POST":
        if "weed_image" not in request.files:
            flash("No file uploaded.")
            return redirect("/newID")
        
        file = request.files["weed_image"]

        if file.filename == "":
            flash("No file selected.")
            return redirect("/newID")
        
        data = {"organs": ["auto"]}

        if file.filename.lower().endswith(".heic") or file.mimetype.startswith("image/hei"):
            converted = convert_heic_to_jpg(file.stream)
            filename_jpg = file.filename.rsplit('.', 1)[0] + ".jpg"
            files = [
                ("images", (filename_jpg, converted, "image/jpeg"))
            ]
        else:
            files = [
                ("images", (file.filename, file.stream, file.content_type))
            ]

        req = requests.Request("POST", url=api_endpoint, files=files, data=data)
        prepared = req.prepare()

        session = requests.Session()
        response = session.send(prepared)
        pprint(response.json())
        if response.status_code == 200:
            data = response.json()
            return render_template("results.html", data=data)
        else:
            flash("Error occurred while processing the image.")
            return redirect("/newID")

    else:
        return render_template("newID.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True) # , host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

