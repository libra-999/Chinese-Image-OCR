from fastapi import FastAPI, UploadFile, File
from PIL import Image
import numpy as np
import pytesseract

app = FastAPI()

@app.post("/ocr/services")
async def recognize(file: UploadFile = File(...)):
    
    image = Image.open(file.file).convert("RGB")    
    image.thumbnail((1200, 1200))

    # Convert to numpy (optional for cropping later)
    img_np = np.array(image)
    text = pytesseract.image_to_string(
        img_np,
        lang="khm+eng"
    )
    
    print(text)
    texts = text.split("\n")

    return {
        "text": 'hello',
        "signature": "hello"
    }