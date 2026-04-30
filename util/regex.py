import re
from datetime import datetime

# Country Mode
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