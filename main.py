from fastapi import FastAPI
from api  import caeser_cipher_controller as csc_router, image_easy_controller as ocr_router
from util.response import httpResp

app = FastAPI()

@app.get("/")
async def main():
    return httpResp(
        code=200,
        message="Service is up",
        data=None
        )

app.include_router(
    csc_router.router,
    prefix="/v2/api"
)
app.include_router(
    ocr_router.router,
    prefix="/v2/api"
)
