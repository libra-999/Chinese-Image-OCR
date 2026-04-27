from fastapi import FastAPI, UploadFile, File, HTTPException
import numpy as np
from PIL import Image, ImageEnhance
import easyocr
import re
from util import chinese_name

app = FastAPI()
reader = easyocr.Reader(
    ['ch_tra','en'],
    gpu=False, # no need support on Mac, khmer language does not support in EasyOCR
)  

## response RestFull
def resp_ocr():
    return {
        "nameZh": "",
        "nameEn": "",
        "genderZh": "",
        "genderEn": "",
        "dob": "",
        "nationalityZh": "",
        "nationalityEn": "",
        "idNumber": "",
        "passportNumber": "",
        "validFrom": "",
        "validTo": "",
        "issueDate": "",
        "address": ""
    }
    
## Country Mode
def detect_country (text: str):
    t = text.upper()
    if "TAIWAN" in t or "ARC" in t:
        return "TW"
    if "HONGKONG" in t or "HONG KONG" in t:
        return "HK"
    if "SINGAPOR" in t  or "PASSPORT" in t:
        return "SG"
    if "CAN" in  t:
        return "CN"
    return 'UNKNOWN'

## check regex
def first_match(pattern, text):
    m = re.search(pattern, text, re.I)
    return m.group(1) if m else ""

## date format
def date_format(text):
    return re.findall(r'(?:19|20)\d{2}[./-]\d{2}[./-]\d{2}', text)

## parse fields
def parse(country, text):
    f = resp_ocr()
    if country == "CN":
        f["nameZh"] = chinese_name(text)
        f["nameEn"] = first_match(r'([A-Z]{4,},?\s+[A-Z]{4,})', text)
    elif country == "HK":
        f["nameEn"] = first_match(r'([A-Z]{4,},?\s+[A-Z]{4,})', text)
        f["nameZh"] = chinese_name(text)
    elif country == "TW":
        f["nameZh"] = chinese_name(text)
        f["nameEn"] = first_match(r'([A-Z]{4,},?\s+[A-Z]{4,})', text)
    elif country == "SG":
        f["nameEn"] = first_match(r'([A-Z]{4,},?\s+[A-Z]{4,})', text)
    return f


@app.post("/ocr/services")
async def recognize(file: UploadFile = File(...)):

    image = Image.open(file.file)
    img_np = np.array(image)
    results = reader.readtext(
        img_np, 
        paragraph=False,
        )
    # print(results)
    texts = [res[1] for res in results]
    raw_text = " ".join(texts)
    country = detect_country(raw_text)
    fields = parse(country,raw_text)
    
    return {
        "success": True,
        "rawText": texts,
        "country": country,
        "fields": fields
    }
    
