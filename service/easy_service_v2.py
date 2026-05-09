from model.easy_ocr import ocr_data
from datetime import datetime
from util.regex import  convert_to_date,date_time_format
import re


def parse_data_v2(country, fields) :
    parse_field = ocr_data.copy()
    if country == "CN":
        return ch_card_v2(fields, parse_field)
    elif country == "TW":
        return tw_card_v2(fields, parse_field)
    elif country == "SG":
        return sg_card_v2(fields, parse_field)
    elif country == "HK":
        return hk_card_v2(fields, parse_field)
    return None
    
def obj_fields_template (fields): 
    return {
        "id": fields.get("idNumber") or "",
        "name": fields.get("name") or "",
        "dob": fields.get("dob") or "",
        "gender": fields.get("gender") or "" ,
        "created_at": fields.get("issuedDate") or "",
        "country": fields.get("country") or ""
    }
    
def ch_card_v2(fields, parse_field):
    map_fields = obj_fields_template(fields)

    parse_field["nameEn"] = re.findall(r'[A-Z]+(?:\s+[A-Z]+)*', map_fields["name"])[0]
    parse_field["nameZh"] = re.findall(r'[\u4e00-\u9fff]+', map_fields["name"])[0]

    parse_field["gender"] = re.search(r'女|男|M|F|male|Male|female|Female|FEMALE|MALE',map_fields["gender"]).group()
    parse_field["dob"] =  re.findall(r'\b(?:\d{4}|\d{2})[./-]\d{2}[./-](?:\d{4}|\d{2})\b', map_fields["dob"])[0]
    parse_field["idNumber"] = map_fields["id"]
    
    issued_at = re.findall(r'\b(?:\d{4}|\d{2})[./-]\d{2}[./-](?:\d{4}|\d{2})\b',map_fields["created_at"])
    parse_issued_at = sorted(datetime.strptime(d,"%Y.%m.%d") for d in issued_at)
    parse_field["validFrom"] =convert_to_date(date_time_format(parse_issued_at[0].strftime("%Y.%m.%d"))) 
    parse_field["validTo"] = convert_to_date(date_time_format(parse_issued_at[1].strftime("%Y.%m.%d")))
    
    parse_field["nationality"] = map_fields["country"]
    return parse_field

def tw_card_v2(fields, parse_field):
    map_fields = obj_fields_template(fields)
    
    parse_field["nameZh"] = re.findall(r'姓名\s*([\u4e00-\u9fff]+)', map_fields["name"])[0]
    
    parse_field["idNumber"] = map_fields["id"]
    parse_field["gender"] = re.search(r'女|男|M|F|male|Male|female|Female|FEMALE|MALE',map_fields["gender"]).group()

    if map_fields["country"] == '':
        parse_field["nationality"] = "Taiwan"
    
    parse_field["dob"] = map_fields["dob"]
    return parse_field

def hk_card_v2(fields, parse_field):
    map_fields = obj_fields_template(fields)
    
    parse_field["nameEn"] = re.findall(r'[A-Z]+,\s+[A-Za-z]+(?:\s+[A-Za-z]+)*', map_fields["name"])[0]
    parse_field["nameZh"] = re.findall(r'[\u4e00-\u9fff]+(?:\s+[\u4e00-\u9fff])*', map_fields["name"])[0]

    parse_field["gender"] = re.search(r'女|男|M|F|male|Male|female|Female|FEMALE|MALE',map_fields["gender"]).group()
    parse_field["dob"] =  re.findall(r'\b(?:\d{4}|\d{2})[./-]\d{2}[./-](?:\d{4}|\d{2})\b', map_fields["dob"])[0]
    parse_field["idNumber"] = map_fields["id"]
    
    if map_fields["country"] == '':
        parse_field["nationality"] = "Hong Kong"
        
    parse_field["validTo"] =  re.findall(r'\b(?:\d{4}|\d{2})[./-]\d{2}[./-](?:\d{4}|\d{2})\b', map_fields["created_at"])[0]

    return parse_field

def sg_card_v2(fields, parse_field):
    map_fields = obj_fields_template(fields)
    
    
    parse_field["nameEn"] = re.findall(r'[A-Z]+(?:\s+[A-Z]+)*', map_fields["name"])[0]
    parse_field["gender"] = re.search(r'女|男|M|F|male|Male|female|Female|FEMALE|MALE',map_fields["gender"]).group()
    parse_field["dob"] =  re.findall(r'\b(?:\d{4}|\d{2})[./-]\d{2}[./-](?:\d{4}|\d{2})\b', map_fields["dob"])[0]
    
    if re.findall(r'Country of Birth\s*([A-Za-z]+)', map_fields["country"])[0] == "SINGAPORE":
        parse_field["nationality"] =  "Singapore"
    else:
        parse_field["nationality"] = re.findall(r'Country of Birth\s*([A-Za-z]+)', map_fields["country"])[0]
    return parse_field
