from fastapi import FastAPI, UploadFile, File
from paddleocr import PaddleOCR
import numpy as np
from PIL import Image

app = FastAPI()
ocrCH = PaddleOCR(
    lang='ch', # language detech (cn + en), note : paddle cannot handle multiple lang in one
    use_angle_cls=True,  # rotation detch
    show_log=False, # cleaner output
    cpu_thread=4 , # limit CPU
    det_limit_side_len=1200, #detct object resize 
)

# run paddle to train image model
@app.post("/ocr/services")
async def recognize(file: UploadFile = File(...)):
    
    image = Image.open(file.file).convert("RGB")
    # pixel verification to reduce more over hit CPU
    image.thumbnail((1200,1200))

    img_np = np.array(image)
    
    # detech normal text
    result_cn_trained = ocrCH.ocr(img_np)
    arrText2= result_cn_trained[0]['rec_texts']
    
    # detech signature by crop
    # h,w, _ = img_np.shape
    # x1 = int(w * 0.65)
    # x2 = int(w * 0.95)
    # y1 = int(h * 0.65)
    # y2 = int(h * 0.92)
    
    # signature_crop = img_np[y1:y2, x1:x2]
    # #convert to base 64
    # pil_img = Image.fromarray(signature_crop)
    # buffer = io.BytesIO()
    # pil_img.save(buffer, format="PNG")
    # signature_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return {"text": arrText2, "signature": 'hello'}