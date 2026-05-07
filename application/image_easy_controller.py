from fastapi import FastAPI,  HTTPException, Body , Header
import numpy as np
from PIL import Image
from util.response import resp_ocr ,httpResp
from service.easy_service import parseData
import cv2
from config.ocr_config import get_reader, client
from io import BytesIO
import requests

app = FastAPI()
@app.post("/ocr/services")
async def recognize(file: dict = Body(...), country: str = Body(...)):
    try:

        file_path = file.get("url")    
    
        if not file_path :
            raise HTTPException(status_code=400, detail="Cannot found filePath")
        elif not country : 
            raise HTTPException(status_code=400, detail="Cannot found country")
        
        response = requests.get(file_path)
        image = Image.open(BytesIO(response.content)).convert("RGB")
        img_np = np.array(image)

        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape     
           
        # improve color contrast for dark image
        mean = gray.mean()
        if mean < 90:            
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8.8))
            gray = clahe.apply(gray)
        
        # improve scale image if it have small width
        if w < 500 and h < 400:
            scale =  2
        elif w < 700 and h < 500:
            scale  = 2.3
        elif w < 1200 and h < 1000:
            scale = 0.90
        gray = cv2.resize(gray, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_CUBIC)
        
        # switch ocr lang by following country
        raw_text, boxes = client(gray, get_reader("simplified"))
        if country in ["TW","HK"]:
            raw_text , boxes  = client(gray, get_reader("traditional"))
        elif country in ["SG"]:
            raw_text , boxes  = client(gray, get_reader("latin"))
            
            
        fields = parseData(country,raw_text,boxes)            
        return httpResp(200,"Succeed",resp_ocr(country,fields,boxes))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
