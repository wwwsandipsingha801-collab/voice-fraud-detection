from fastapi import FastAPI, UploadFile
import shutil
import sys
import os

# 👉 important fix (path issue solve karega)
sys.path.append(os.path.abspath("."))

from features.feature_extractor import extract_features
from model.model import predict

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Voice Fraud Detection API Running"}


@app.post("/analyze")
async def analyze(file: UploadFile):
    file_path = "temp.wav"

    # file save karna
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # feature extraction
    mfcc, spec = extract_features(file_path)

    # prediction
    result = predict(mfcc, spec)

    return {"result": result}