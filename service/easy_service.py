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

# date of birth with same format
def field_date (box, fields):
    date =  []
    for t in box :
        dob_match = re.findall(r'\b(?:\d{4}|\d{2})[./-]\d{2}[./-](?:\d{4}|\d{2})\b',t)
        date.extend(dob_match)

    print(json.dumps(date))
    if len(date) >=1 :
        fields["dob"] = date_time_format(date[0])
    if len(date) >= 2 :
        fields["validFrom"] = date_time_format(date[1])
    if len(date) >= 3:
        fields["validFrom"] = date_time_format(date[3])
        fields["validTo"] = date_time_format(date[2])
    return fields

# gender with same format
def field_gender (box, fields):
    fields["gender"] = "" 
    for t in box:
        if re.search(r'女|\bF\b|\bFemale\b|\bFEMALE\b',t,re.I):
            fields["gender"] = "F"
            break
        elif  re.search(r'男|\bM\b|\bMale\b|\bMALE\b',t, re.I):
            fields["gender"] = "M"
    return fields

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
    
    for t in box:
        match = match_text_with_box(r'[\u4e00-\u9fff]+(?:\s[\u4e00-\u9fff]+)*',t, text)
        if match:
            fields["nameZh"] = match
            break

    name_part = []
    for t in  box:
        match = match_text_with_box(r'[A-Z]{2,10}+(?:\s[A-Z]{2,10}+)*',t, text)
        if match :
            name_part.append(match)
    fields["nameEn"] = " ".join(name_part)
    
    for t in box:
        match = match_text_with_box(r'\d{17,18}', t,text)
        if  match:
            fields["idNumber"] = match
            break
        
    fields = field_date(box, fields)
    fields = field_gender(box, fields)

    for t in box:
        if re.fullmatch(r'[A-Z]{3}',t):
            fields["nationality"] = t
            break
    
    fields["nationality"] = "Chinese"    
        
    return fields

# Singapor
def sg_card(text, box, fields):
    
    text_box_joined = " ".join(box) 
    match  = re.search(r'\bName\b\s*(.*?)\s*(?:[\u4e00-\u9fff])', text_box_joined, re.I)
    if match :
        fields["nameEn"] = match.group(1).strip()
     
    for t in box:
        match =  match_text_with_box(r'[\u4e00-\u9fff]+\s+[\u4e00-\u9fff]+\s+[\u4e00-\u9fff]', t,text)
        if match :
            fields["nameZh"] = match
            break
      
    for t in box:
        match = match_text_with_box(r'[A-Z]?\d{6,9}[A-Z]?', t, text)
        if match:
            fields["idNumber"] = match
            break
        
    fields = field_date(box,fields)   
    fields = field_gender(box,fields)
    fields["nationality"] = "Singapor"
    return fields

#Hong Kong
def hk_card(text,box, fields):
    
    for t in box:
        match = match_text_with_box(r'[A-Z]?\d{6,7}\([A-Z]?\d{1}\)', t, text)
        if match :
            fields["idNumber"] = match
            break

    for t in box:
        match =  match_text_with_box(r'[\u4e00-\u9fff]+\s[\u4e00-\u9fff]+(?:\s?[\u4e00-\u9fff]+)*', t,text)
        if match :
            fields["nameZh"] = match
            break
        
    for t in box:
        match =  match_text_with_box(r'[A-Z]{2,},\s?[A-Z][a-z]+(?:\s[A-Z][a-z]+)*', t, text)
        if match :
            fields["nameEn"] = match
            break   
         
    fields = field_date(box, fields)
    fields = field_gender(box,fields)    
            
    fields["nationality"] = "HongKong"
    return fields
