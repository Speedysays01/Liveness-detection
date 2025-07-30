from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from PIL import Image
from io import BytesIO

app = FastAPI()

class ImageURL(BaseModel):
    url: str

@app.post("/check-liveness/")
async def check_liveness_url(data: ImageURL):
    try:
        response = requests.get(data.url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Image couldn't be downloaded.")

        image = Image.open(BytesIO(response.content))
        # Here you’ll later add your actual model prediction logic
        return {"result": "real"}  # dummy response for now

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
