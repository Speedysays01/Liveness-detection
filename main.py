from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import shutil
import uuid
import os

# Initialize FastAPI app
app = FastAPI()

# Define the request body model
class ImageURL(BaseModel):
    url: str

# Dummy anti-spoofing module for now — replace with your actual import
class AntiSpoofing:
    def predict(self, image_path):
        # Replace this with actual prediction logic
        return "real"  # or "spoof"

anti_spoofing = AntiSpoofing()

@app.post("/predict-url")
async def predict_url(data: ImageURL):
    image_url = data.url

    try:
        # Create a temporary file name
        filename = f"temp_{uuid.uuid4()}.jpg"

        # Download image from the URL
        response = requests.get(image_url, stream=True)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Image download failed")

        # Save the downloaded image
        with open(filename, "wb") as out_file:
            shutil.copyfileobj(response.raw, out_file)

        # Run prediction
        result = anti_spoofing.predict(filename)

        # Delete temporary image
        os.remove(filename)

        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
