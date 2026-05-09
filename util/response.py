def resp_ocr(country,ocr_data,box):
    return {
        "country": country,
        "fields": ocr_data,
        "box": box
    }
    
def httpResp (code: int, message: str, data): 
    return {
        "code": code,
        "message": message,
        "data": data
    }