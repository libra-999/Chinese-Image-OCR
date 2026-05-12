import requests
from PIL import Image
import cv2
from util.regex import crop_field_by_country
from service.easy_service_v2 import parse_data_v2
from util.exception import  bad_request
import v1.ocr_image_pb2 as data_pb2
import v1.ocr_image_pb2_grpc as data_pb2_grpc
from service.easy_service_v2 import parse_data_v2
import numpy as np
from io import BytesIO
from config.ocr_config import get_reader, client , TEMPLATE
from model.easy_ocr import ocr_data

class ImageOCRService(data_pb2_grpc.ImageOCRServiceServicer):
    def UploadImageServer(self, request, context):
        
        country = request.country  
        url = request.url  
        
        response = requests.get(url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content)).convert("RGB")
        img_np = np.array(image)  
        
        if img_np is None or img_np.size == 0:
            bad_request(400,"Num py is None")
                
        gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
        mean = gray.mean()
        if mean < 90:            
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8.8))
            gray = clahe.apply(gray)   
            
        if country in  ["TW", "HK"]:
            reader = get_reader("traditional")
        elif country in ["SG"]:
            reader = get_reader("latin")
        elif country in ["KH"]:
            reader = get_reader("khmer")
        elif country in ["CN"]:
            reader = get_reader("simplified")

        gray = cv2.resize(gray, (1200,900), interpolation=cv2.INTER_CUBIC)
        template = TEMPLATE.get(country)
        fields  = {}
        
        for name , coords in template.items():
            if coords is None:
                fields[name] = ""
                continue
            
            crop = crop_field_by_country(gray, coords)
            text, box = client(crop, reader)
            fields[name] = text
        
        
        fields = parse_data_v2(country,fields)
        ocr_fields = data_pb2.OCRData(
            idNumber=fields.get("idNumber") or "",
            nameZh=fields.get("nameZh") or "",
            nameEn=fields.get("nameEn") or "",
            gender=fields.get("gender") or "",
            dob=fields.get("dob") or "",
            nationality=fields.get("nationality") or "",
            validFrom=fields.get("validFrom") or "",
            validTo=fields.get("validTo") or "",
            address=fields.get("address") or "",
        )
        return data_pb2.ImageOCRResp(
            country=country,
            fields=ocr_fields
        )