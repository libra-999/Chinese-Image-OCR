import re

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