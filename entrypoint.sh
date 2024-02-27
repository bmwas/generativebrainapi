#!/bin/bash
set -xe
cd /app/MONAI/MonaiGenerativeModels
source activate monai
exec uvicorn main:app --reload --workers 4 --host 0.0.0.0 --port 8000

