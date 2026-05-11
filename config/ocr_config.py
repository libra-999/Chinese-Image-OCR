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

# crop fields
TEMPLATE = {
    "CN": {
        "idNumber": (397, 681,945, 723),
        "name": (165, 245, 580, 342),
        "dob": (396, 373, 621, 451),
        "gender": (166, 366, 269, 456),
        "issuedDate": (169,617,554,650),
        "country": (170, 513, 376, 556),
    },
    "TW": {
        "idNumber": (781,744,1125,816),
        "name": (62,426,601,514),
        "dob": (318,604,704,670),
        "gender": (868,617,1033,680),
        "issuedDate": None,
        "country": None

    },
    "SG": {
        "idNumber": (441,125,764,170),
        "name": (265,341,922,532),
        "dob": (275,682,496,718),
        "gender": (635,678,670,719),
        "issuedDate": None,
        "country": (272,781,490,815)
    },
    "HK": {
        "idNumber": (820,781,1156,837),
        "name": (63,181,474,319),
        "dob": (466,454,776,564),
        "gender": (778,507,856,571),
        "issuedDate": (464,643,777,844),
        "country": None
    }
}

@lru_cache(maxsize=4) # store only 2 process , one is 'traditional' and other one is 'simplified'
def get_reader(lang_code):
    if lang_code == "traditional":
        return  easyocr.Reader(["ch_tra","en"], gpu=False) # tw , hk
    elif lang_code == "simplified":
        return easyocr.Reader(["ch_sim","en"], gpu=False) # cn
    elif lang_code == "latin": 
        return easyocr.Reader(["en","ch_sim"], gpu=False) # sg
    else: 
        return easyocr.Reader(["en"], gpu=False)

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

        if text:
            texts.append(text)
            boxes.append({
                "text": text,
                "confidence": conf,
                "box": [[int(x) , int(y)] for x , y in box]
            })

    return " ".join(texts),boxes
   