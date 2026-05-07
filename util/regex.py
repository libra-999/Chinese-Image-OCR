import re
from datetime import datetime

# Country Mode
def detect_country (text: str):
    t = text.upper()
    if "TAIWAN" in t or "ARC" in t:
        return "TW"
    if "HONGKONG" in t or "HONG KONG" in t:
        return "HK"
    if "SINGAPOR" in t:
        return "SG"
    if "CAN" in t or "中文" in  t:
        return "CN"
    return 'UNKNOWN'

# fullmatch check 
def match_text_with_box(regex, box_text , standard_text ) :
    if re.fullmatch(regex , box_text):
        if box_text in standard_text:
            return box_text
    return ""

# date format
def date_time_format(date) :
    if not date:
        return ""
    
    date = date.strip() # like a trim()
    date = re.sub(r'\s+', '',date)
    date  = date.replace(".","-").replace("/","-")
    
    formats = [
        "%Y-%m-%d", # 2022-12-19
        "%d-%m-%Y", # 19-12-2022
        "%d-%m-%y", # 19-12-22
    ]
    for fmt in formats:
        try:
            parsed = datetime.strptime(date, fmt)
            return parsed.strftime("%d-%m-%Y")
        except ValueError:
            continue
    return date

# convert to type date
def convert_to_date(date: str) :
    if date == "":
        return None
    return datetime.strptime(date, "%d-%m-%Y")

# order field box left to right and top to bottom
def get_xy(result):
    box = result[0]
    xs = [p[0] for p in box]
    ys = [p[1] for p in box]
    return min(xs), min(ys)

def reorder_by_line(results, gap=15):
    rows = []
    for r in results:
        x, y = get_xy(r)
        found = False
        for row in rows:
            if abs(row["y"] - y) <= gap:
                row["items"].append((x, r))
                found = True
                break
        if not found:
            rows.append({
                "y": y,
                "items": [(x, r)]
            })

    rows.sort(key=lambda row: row["y"])
    final = []
    for row in rows:
        row["items"].sort(key=lambda t: t[0])   # left to right
        final.extend([item[1] for item in row["items"]])

    return final


def crop_field_by_country (img ,coordinate):
    x1,y1,x2,y2 = coordinate
    return img[y1:y2, x1:x2]