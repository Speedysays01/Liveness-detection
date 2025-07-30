from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import shutil

# Add this near top if not already present
import uuid
import os

class ImageURL(BaseModel):
    url: str

@app.post("/predict-url")
async def predict_url(data: ImageURL):
    image_url = data.url

    try:
        # Download image from URL
        filename = f"temp_{uuid.uuid4()}.jpg"
        response = requests.get(image_url, stream=True)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Image download failed")

        with open(filename, "wb") as out_file:
            shutil.copyfileobj(response.raw, out_file)

        # Run prediction
        result = anti_spoofing.predict(filename)

        # Clean up
        os.remove(filename)

        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
