# url = "https://plant.id/api/v3/identification"
# API_KEY = os.getenv("PLANT_ID_API_KEY") # get from env var for security

if request.method == "POST":
        # Get the uploaded file
        file = request.files["weed_image"]
        if file:
            file_bytes = file.read()
            image_base64 = base64.b64encode(file_bytes).decode('utf-8')
            payload = json.dumps({"images": [image_base64], "similar_images": True})
            headers = {
                "Content-Type": "application/json",
                "Api-Key": API_KEY
            }
            # Send the file to the Plant.id API for identification
            response = requests.request("POST", url, headers=headers, data=payload)
            # data = response.json()
            data = {"access_token": "3xNjab0HQgNdKbY", "model_version": "plant_id:5.0.0", "custom_id": None, "input": {"latitude": None, "longitude": None, "images": ["https://plant.id/media/imgs/62425dcde04a4ac284b8cbdac3e0207d.jpg"], "datetime": "2025-08-08T19:22:25.937974+00:00"}, "result": {"classification": {"suggestions": [{"id": "d5546bd31bdd3e76", "name": "Glycine max", "probability": 0.0704, "details": {"language": "en", "entity_id": "d5546bd31bdd3e76"}}, {"id": "cffe9687ffd904ac", "name": "Neustanthus phaseoloides", "probability": 0.0344, "details": {"language": "en", "entity_id": "cffe9687ffd904ac"}}, {"id": "2dda2d6da56f9959", "name": "Phaseolus vulgaris", "probability": 0.0261, "details": {"language": "en", "entity_id": "2dda2d6da56f9959"}}, {"id": "309b2b1888609d1f", "name": "Amaranthus blitum", "probability": 0.0236, "details": {"language": "en", "entity_id": "309b2b1888609d1f"}}, {"id": "162623cdbeeb3def", "name": "Senna", "probability": 0.0235, "details": {"language": "en", "entity_id": "162623cdbeeb3def"}}]}, "is_plant": {"probability": 0.9925833, "threshold": 0.5, "binary": True}}, "status": "COMPLETED", "sla_compliant_client": True, "sla_compliant_system": True, "created": 1754680945.937974, "completed": 1754680946.188345}
            return render_template("results.html", data=data)
        else:
            flash("No file uploaded.")
        return render_template("results.html")