from fastapi import FastAPI, UploadFile
import shutil
import sys
import os

# fix import path
sys.path.append(os.path.abspath("."))

from features.feature_extractor import extract_features
from model.model import predict

# 👉 THIS LINE WAS MISSING
app = FastAPI()


@app.get("/")
def home():
    return {"message": "Voice Fraud Detection API Running"}


@app.post("/analyze")
async def analyze(file: UploadFile):
    file_path = "temp.wav"

    # save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # feature extraction
    mfcc, spec = extract_features(file_path)

    # DEBUG
    print("MFCC shape:", mfcc.shape)
    print("Spectrogram shape:", spec.shape)

    # prediction
    result = predict(mfcc, spec)

    # DEBUG
    print("Prediction result:", result)

    return {"result": result}