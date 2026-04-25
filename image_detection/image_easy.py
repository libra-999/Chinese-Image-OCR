from fastapi import FastAPI, UploadFile, File
import numpy as np
from PIL import Image
import easyocr

app = FastAPI()
reader = easyocr.Reader(['ch_tra','en'], gpu=False)  # Khmer not supported

@app.post("/ocr/services")
async def recognize(file: UploadFile = File(...)):
    
    image = Image.open(file.file).convert("RGB")
    
    # Resize to reduce CPU usage
    image.thumbnail((1200, 1200))

    img_np = np.array(image)

    # Run OCR
    results = reader.readtext(img_np)

    # Extract only text
    texts = [res[1] for res in results]
    print(texts)
    return {
        "text": 'text',
        "signature": "hello"
    }