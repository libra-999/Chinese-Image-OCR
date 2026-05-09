from fastapi import HTTPException, Header

def server_internal(code: int, msg: str):
    raise HTTPException(status_code=code,detail=msg)

def bad_request(code= None, msg: str= ""):
    if code is None:
        code = 400
    raise HTTPException(status_code=code, detail=msg)

def not_found(code=None, msg:str = ""):
    if code is None:
        code = 404
    raise HTTPException(status_code=code, detail=msg)
    