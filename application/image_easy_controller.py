from fastapi import FastAPI, UploadFile, File, HTTPException
import numpy as np
import easyocr
from PIL import Image
from util.regex  import detect_country
from util.response import resp_ocr ,httpResp
from service.easy_service import parseData
import cv2

app = FastAPI()
reader = easyocr.Reader(
    ['ch_sim','en'],  # ch_tra more accurancy with 'tw' & 'hk' and ch_sim 'cn' & 'sg' 
    gpu=False, # no need support on Mac, khmer language does not support in EasyOCR
)  
    
@app.post("/ocr/services")
async def recognize(file: UploadFile = File(...)):
    try:
        image = Image.open(file.file).convert("RGB")
        img_np = np.array(image)

        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

        # resize text to bigger
        h, w = gray.shape
        scale = 1200 / w if w < 1200 else 1
        gray = cv2.resize(gray, (int(w * scale), int(h * scale)))

        # sharpen
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        results = reader.readtext(
            gray,
            paragraph=False,
            detail=1,
            width_ths=0.8,
            height_ths=0.3,
            contrast_ths=0.05,
            adjust_contrast=0.7,
            text_threshold=0.6,
            low_text=0.3
        )

        texts = []
        boxes = []

        results = sorted(results, key=lambda r: (r[0][0][1], r[0][0][0]))
        for res in results:
            box = res[0]
            text = res[1].strip()
            conf = float(res[2])

            # remove weak confidence garbage
            if conf < 0.35:
                continue

            if text:
                texts.append(text)
                boxes.append({
                    "text": text,
                    "confidence": conf,
                    "box": [[int(x) , int(y)] for x , y in box]
                })

        raw_text = " ".join(texts)
        country = detect_country(raw_text)
        fields = parseData(country,raw_text,boxes)            

        return httpResp(200,"Succeed",resp_ocr(country,fields,boxes))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))