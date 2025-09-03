import io, os
from typing import Optional
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel
from PIL import Image
from detector import detect_image_safe, detect_image_strict, detect_text_safe, detect_text_strict

APP_VERSION = "v3.2"
MAX_UPLOAD = int(os.getenv("MAX_UPLOAD_MB","10"))*1024*1024

app = FastAPI(title="Intimate Detector Prototype API", version=APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def limit_upload_size(request, call_next):
    if request.headers.get("content-length"):
        if int(request.headers["content-length"]) > MAX_UPLOAD:
            return PlainTextResponse("Request too large", status_code=413)
    return await call_next(request)

@app.post("/api/detect-image")
async def detect_image(file: UploadFile = File(...), threshold: float = Form(0.5), strict: bool = Form(False)):
    content = await file.read()
    try:
        Image.open(io.BytesIO(content)).verify()
    except Exception:
        pass
    result = detect_image_strict(content, threshold) if strict else detect_image_safe(content, threshold)
    return JSONResponse(content={**result,"model_version":APP_VERSION,"threshold":threshold})

class TextRequest(BaseModel):
    text: str
    threshold: Optional[float] = 0.5
    strict: Optional[bool] = False

@app.post("/api/detect-text")
async def detect_text_api(req: TextRequest):
    result = detect_text_strict(req.text, req.threshold) if req.strict else detect_text_safe(req.text, req.threshold)
    return JSONResponse(content={**result,"model_version":APP_VERSION,"threshold":req.threshold})

@app.get("/health")
async def health():
    return {"ok":True,"model_loaded":True,"version":APP_VERSION}
