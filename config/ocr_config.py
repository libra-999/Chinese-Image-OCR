from functools import lru_cache
import easyocr
from util.regex import reorder_by_line

# confidential config to improve output
OCR_CONFIG = {
    "paragraph":False,
    "detail":1,
    "width_ths":0.8,
    "height_ths":0.3,
    "contrast_ths":0.1,
    "adjust_contrast":0.7,
    "text_threshold":0.45,
    "low_text":0.15
}

@lru_cache(maxsize=3) # store only 2 process , one is 'traditional' and other one is 'simplified'
def get_reader(lang_code):
    if lang_code == "traditional":
        return  easyocr.Reader(["ch_tra","en"], gpu=False) # tw , hk
    elif lang_code == "simplified":
        return easyocr.Reader(["ch_sim","en"], gpu=False) # cn
    else: 
        return easyocr.Reader(["en","ch_sim"], gpu=False) # sg

# engine
def client(gray, reader):
    results = reader.readtext(
            gray,
            OCR_CONFIG
        )

    results = reorder_by_line(results)
    texts = []
    boxes = []

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

    return " ".join(texts),boxes
   