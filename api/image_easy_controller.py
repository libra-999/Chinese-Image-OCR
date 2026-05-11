from fastapi import Body , UploadFile, File , APIRouter, Form
import numpy as np
from PIL import Image
from util.response import resp_ocr ,httpResp
from util.regex import crop_field_by_country
from service.easy_service_v2 import parse_data_v2
from util.exception import server_internal , bad_request, not_found
from model.enum.country_constant import CountryEnum

import cv2
from config.ocr_config import get_reader, client , TEMPLATE
from io import BytesIO
import requests

router = APIRouter(
    prefix="/ocr",
    tags=["OCR KYC"],
    # responses={not_found(404,"Not Found")}
)

@router.post("/services")
async def recognize(file: UploadFile = File(...), country: CountryEnum = Form(...)):
    try:
        # file_path = file.get("url")    
    
        if file is None :
            bad_request(400,"File cannot be null")
        elif country not in CountryEnum or country is "": 
            bad_request(400,"Country cannot be null")
        
        # response = requests.get(file_path)
        content = await file.read()
        image = Image.open(BytesIO(content)).convert("RGB")
        img_np = np.array(image)  
        
        if img_np is None or img_np.size == 0:
            bad_request(400,"Num py is None")
                
        # improving image color and size
        gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
        mean = gray.mean()
        if mean < 90:            
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8.8))
            gray = clahe.apply(gray)   
            
        # country call to client by manage with custom service    
        if country in  ["TW", "HK"]:
            reader = get_reader("traditional")
        elif country in ["SG"]:
            reader = get_reader("latin")
        elif country in ["KH"]:
            reader = get_reader("khmer")
        elif country in ["CN"]:
            reader = get_reader("simplified")

        # resize image by scale with 1200 * 900 (default)
        gray = cv2.resize(gray, (1200,900), interpolation=cv2.INTER_CUBIC)
        template = TEMPLATE.get(country)
        fields = {}
        
        for name , coords in template.items():
            # keep process even it doesn't have position 
            if coords is None:
                fields[name] = ""
                continue
            
            crop = crop_field_by_country(gray, coords)
            text, box = client(crop, reader)
            fields[name] = text
        
        data = parse_data_v2(country, fields) 
        if data is None :
            bad_request(400,"Empty Data! ,it can be you provide wrong country from list")

        return httpResp(200,"Succeed", data)

    except Exception as e:
        server_internal(500,str(e))
