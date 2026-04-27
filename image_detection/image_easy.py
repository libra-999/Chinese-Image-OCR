from fastapi import FastAPI, UploadFile, File, HTTPException
import numpy as np
import easyocr
from util.regex  import *
from util.response import *

app = FastAPI()
reader = easyocr.Reader(
    ['ch_tra','en'],
    gpu=False, # no need support on Mac, khmer language does not support in EasyOCR
)  


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
    
    print(results)
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
    
