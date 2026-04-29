from fastapi import FastAPI, UploadFile, File, HTTPException
import numpy as np
from PIL import Image
from util.regex  import detect_country
from util.response import resp_ocr ,httpResp
from service.easy_service import parseData
import cv2
from config.ocr_config import ocr_engin, get_reader
import json

app = FastAPI()
@app.post("/ocr/services")
async def recognize(file: UploadFile = File(...)):
    try:
        image = Image.open(file.file).convert("RGB")
        img_np = np.array(image)

        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

        # resize text to bigger
        h, w = gray.shape
        
        print(f"Height: {h}, Width: {w}")
        target_width =  1200 if w < 1200 else w
        scale = target_width / w if w < target_width else 1   
        gray = cv2.resize(gray, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_CUBIC)
        
        new_h , new_w =  gray.shape
        print(f"After Height: {new_h}, Width: {new_w}")
        # gray = cv2.GaussianBlur(gray, (3, 3), 0) # little nosie after scale 
        
        # switch ocr lang by following country
        raw_text, boxes = ocr_engin(gray, get_reader("simplified"))
        country = detect_country(raw_text)
        if country in ["TW","HK"]:
            raw_text , boxes  = ocr_engin(gray, get_reader("traditional"))
            country = detect_country(raw_text)
        elif country in ["SG"]:
            raw_text , boxes  = ocr_engin(gray, get_reader("latin"))
            country = detect_country(raw_text) 
            
        # print("Output:" , json.dumps(raw_text))
        fields = parseData(country,raw_text,boxes)            
        return httpResp(200,"Succeed",resp_ocr(country,fields,boxes))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
