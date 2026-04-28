import re
from model.easy_ocr import ocr_data
from util.regex import chinese_name_filter, english_name_filter

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
        return hk_card(text, boxes_text ,f )
    return 


# Taiwin
def tw_card(text, box, fields):
    fields["nameEn"] =  chinese_name_filter(text)
    fields["nameZh"] = english_name_filter(text)
    
     # ID Card
    for t in box:
        if re.fullmatch(r'\b\d{4,17}[\dXx]\b', t):
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
        
    return

# China Simplified
def ch_card(text, box, fields):
    fields["nameZh"] = chinese_name_filter(text)
    fields["nameEn"] = english_name_filter(text)
    return 

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
    return

#Hong Kong
def hk_card(text,box, fields):
    fields["nameEn"] =  chinese_name_filter(text)
    fields["nameZh"] = english_name_filter(text)
    return
