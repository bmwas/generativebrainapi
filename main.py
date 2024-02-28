from fastapi import FastAPI, HTTPException, status, Depends,UploadFile,File,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from functions.genimage import generativeexecutecommand
from typing import Dict, Any
import logging
import base64
from io import BytesIO
from fastapi.responses import FileResponse
import io
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("uvicorn")

#Load API keys
API_KEYS = os.getenv("API_KEYS")

app = FastAPI()
model_name = "Image Generation Microservice/API"
version = "v1.0.0"

   
## doing a simple indexing therefore no need for model(indexing "whole" documents without chunking)
class GenAgeVenBrVolInputData(BaseModel):
    mriid: str= "0124"
    gender: float = 0.0
    age: float = 0.1
    ventricular_vol: float = 0.2
    brain_vol: float =  0.4
    bucket_name: str = "testniis"
    bucket_folder: str = "ldm"


class GenAgeVenBrVolProgress(BaseModel):
    genageventbrainvol_progress: dict


@app.get("/")
def index():
    return {
        "message": "Endpoint to support generation of novel images given a set of population conditions."
    }

@app.get("/health")
async def service_health():
    """Return service health"""
    return {"status": "ok"}


@app.get("/info")
async def model_info():
    """Return model information, version, how to call"""
    return {"name": model_name, "version": version}


def validate_api_key(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))):
    """Validate the API key."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API Key",
        )
    if credentials.scheme != "Bearer" or credentials.credentials not in API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API Key",
        )


@app.post("/generategenderageventbrainvol")
async def input_index_main_text_document(
    data: GenAgeVenBrVolInputData,
    credentials: HTTPAuthorizationCredentials = Depends(validate_api_key)
):
    """Index whole documents...."""
    config_file = "./model-zoo/models/brain_image_synthesis_latent_diffusion_model/configs/generategenderageventbrainvol_inference.json"
    output_folder = "/app/MONAI/GenerativeModels/model-zoo/models/brain_image_synthesis_latent_diffusion_model/output/"
    #bucket_name = "testniis"    
    genageventbrainvol_progress = generativeexecutecommand(data.bucket_name,data.bucket_folder,output_folder,config_file,data.gender,data.age,
        data.ventricular_vol,data.brain_vol)
    output = GenAgeVenBrVolProgress(genageventbrainvol_progress=genageventbrainvol_progress)  # Convert result to str
    return output


origins = [
    "http://localhost",
    "http://localhost:5173",
    "...Your Domains..."
] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 