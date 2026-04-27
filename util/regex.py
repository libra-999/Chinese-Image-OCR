import re

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

## Chinese issue while ocr 
def chinese_name (text) -> str:
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