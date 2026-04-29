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
    
# messy data after ocr
def chinese_name_filter (text) -> str:
    words =  re.findall(r'[\u4e00-\u9fff]{2,6}',text)
    error_fields_chinese_name = [
        "姓名", "莊名",
        "証件", "樣本", "証件樣本",
        "出生日期", "出生", "日期",
        "國籍", "有效期限", "有效", "期限",
        "性別", "香港永久性居民身份證",
        "加拿大", "中國", "美國"
    ]
    
    for word in words:
        word = word.strip()
        if word not in error_fields_chinese_name:
            continue
        if 2 <= len(word) <= 4:
            return word
    return ""    
def english_name_filter(text):
    words = re.findall(r'[A-Za-z]{2,6}', text) # map data to with find all character with upper and lower
    word_messy_list = {
        "CAN", "CHN", "HK", "TW", "SG","FEMALE", "MALE", "DATE", "BIRTH"
    }
    
    words = [w for w in word_messy_list 
                if w not in words]
    if len(words) >= 2:
        return words[-2] + " " + words[-1]
    elif len(words) == 1:
        return words[0]
    return ""
