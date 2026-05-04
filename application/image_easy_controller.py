from fastapi import FastAPI,  HTTPException, Body
import numpy as np
from PIL import Image
from util.regex  import detect_country
from util.response import resp_ocr ,httpResp
from service.easy_service import parseData
import cv2
from config.ocr_config import ocr_engin, get_reader
from io import BytesIO
import requests

app = FastAPI()
@app.post("/ocr/services")

async def recognize(file: dict = Body(...)):
    try:

        file_path = file.get("url")    
        if not file_path:
            raise HTTPException(status_code=400, detail="Cannot found filePath")
        
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
        if w < 1200:
            scale =  2.0
        elif w < 1800:
            scale =  1.3
        else :
            scale = 1.0
        gray = cv2.resize(gray, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_CUBIC)
        
        # switch ocr lang by following country
        raw_text, boxes = ocr_engin(gray, get_reader("simplified"))
        country = detect_country(raw_text)
        if country in ["TW","HK"]:
            raw_text , boxes  = ocr_engin(gray, get_reader("traditional"))
            country = detect_country(raw_text)
        elif country in ["SG"]:
            raw_text , boxes  = ocr_engin(gray, get_reader("latin"))
            country = detect_country(raw_text) 
            
        fields = parseData(country,raw_text,boxes)            
        return httpResp(200,"Succeed",resp_ocr(country,fields,boxes))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
