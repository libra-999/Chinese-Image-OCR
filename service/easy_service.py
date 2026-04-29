import re
from model.easy_ocr import ocr_data
import json
from util.regex import chinese_name_filter, english_name_filter, match_text_with_box , date_time_format

def parseData(country, text, boxes):
    f = ocr_data.copy()
    
    # map to text in box methods 
    boxes_text = [ b["text"].strip() for b in boxes if b["text"].strip() ]
    
    if country == "CN" :
        return ch_card(text,boxes_text, f)   
    elif country == "TW":
        return tw_card(text, boxes_text, f)
    elif country == "SG":
        return sg_card(text, boxes_text, f) 
    elif country == "HK": 
        return hk_card(text, boxes_text, f)
    return ""

# Taiwin
def tw_card(text, box, fields):
    fields["nameEn"] =  chinese_name_filter(text)
    fields["nameZh"] = english_name_filter(text)
    
    # ID Card
    for t in box:
        if re.fullmatch(r'[A-Z][A-Z]\d{7,10}', t):
            fields["idNumber"] = t
            break
        
    dates = re.findall(r'(?:19|20)\d{2}[./-]\d{2}[./-]\d{2}', text)
    if len(dates) >= 1:
        fields["dob"] = dates[0]
    if len(dates) >= 3:
        fields["validFrom"] = dates[1]
        fields["validTo"] = dates[2]
    elif len(dates) == 2:
        fields["validFrom"] = dates[0]
        fields["validTo"] = dates[1]
        
    nat_match = re.search(r'\b[A-Z]{3}\b', text)
    if nat_match:
        fields["nationality"] = nat_match.group()
    if re.search(r'\bF\b|Female', text, re.I):
        fields["gender"] = "F"
    elif re.search(r'\bM\b|Male', text, re.I):
        fields["gender"] = "M"
    
    # national 
    for t in box:
        if re.fullmatch(r'[A-Z]{3}',t):
            fields["nationality"] = t
            break
    # gender
    for t in box:
        if t.upper() in ["F","Female","FEMALE"]:
            fields["gender"] = "F"
            break
        elif t.upper() in ["M","MALE","Male"]:
            fields["gender"] = "M"
            break
        
    return fields

# China Simplified
def ch_card(text, box, fields):
    fields["nameZh"] = chinese_name_filter(text)
    fields["nameEn"] = english_name_filter(text)
    
    # ID Card
    for t in box:
        if re.fullmatch(r'\d{18}', t):
            fields["idNumber"] = t
            break
        
    dates = re.findall(r'(?:19|20)\d{2}[./-]\d{2}[./-]\d{2}', text)
    if len(dates) >= 1:
        fields["dob"] = dates[0]
    if len(dates) >= 3:
        fields["validFrom"] = dates[1]
        fields["validTo"] = dates[2]
    elif len(dates) == 2:
        fields["validFrom"] = dates[0]
        fields["validTo"] = dates[1]
        
    nat_match = re.search(r'\b[A-Z]{3}\b', text)
    if nat_match:
        fields["nationality"] = nat_match.group()
    if re.search(r'\bF\b|Female', text, re.I):
        fields["gender"] = "F"
    elif re.search(r'\bM\b|Male', text, re.I):
        fields["gender"] = "M"
    
    # national 
    for t in box:
        if re.fullmatch(r'[A-Z]{3}',t):
            fields["nationality"] = t
            break
    # gender
    for t in box:
        if t.upper() in ["F","Female","FEMALE"]:
            fields["gender"] = "F"
            break
        elif t.upper() in ["M","MALE","Male"]:
            fields["gender"] = "M"
            break
    return fields

# Singapor
def sg_card(text, box, fields):
    name_1 = []
    for b in box:
        if re.fullmatch(r'[A-Z ]{6,}', b):
            if len(b.split()) >= 2:
                name_1.append(b)
        if name_1 :
            fields["nameEn"] = max(name_1,key=len)
        else: 
            fields["nameEn"] = english_name_filter(text)
    # number ID        
    for t in box:
        if re.fullmatch(r'[A-Z]?\d{7,8}[A-Z]?', t):
            print(t)
            fields["idNumber"] = t
            break
    return fields

#Hong Kong
def hk_card(text,box, fields):
    
    # ID card
    for t in box:
        match = match_text_with_box(r'[A-Z]?\d{6,7}\([A-Z]?\d{1}\)', t, text)
        if match :
            fields["idNumber"] = match
            break
    # Chinese's name card
    for t in box:
        match =  match_text_with_box(r'[\u4e00-\u9fff]+\s[\u4e00-\u9fff]+(?:\s?[\u4e00-\u9fff]+)*', t,text)
        if match :
            fields["nameZh"] = match
            break
    # English's name card
    for t in box:
        match =  match_text_with_box(r'[A-Z]{2,},\s?[A-Z][a-z]+(?:\s[A-Z][a-z]+)*', t, text)
        if match :
            fields["nameEn"] = match
            break    
    # Dob and Issued 
    date =  []
    for t in box :
        dob_match = re.findall(r'\b\d{2}[./-]\d{2}[./-](?:\d{4}|\d{2})\b',t)
        date.extend(dob_match)

    if len(date) >= 2 :
        fields["dob"] = date_time_format(date[0])
        fields["validFrom"] = date_time_format(date[1])
    elif len(date) >= 3:
        fields["dob"] = date_time_format(date[0])
        fields["validFrom"] = date_time_format(date[1])
        fields["validTo"] = date_time_format(date[2])
        
    # Gender 
    for t in box:
        
        female = re.search(r'女|\bF\b|\bFemale\b|\bFEMALE\b',t)
        male = re.search(r'男|\bM\b|\bMale\b|\bMALE\b',t)
        
        if female:
            fields["gender"] = "F"
            break
        elif male:
            fields["gender"] = "M"
            break
        else :
            fields["gender"] = ""

    return fields
