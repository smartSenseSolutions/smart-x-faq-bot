import os
import shutil
from enum import Enum
from pathlib import Path

import pandas as pd
from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile
from pydantic import BaseModel

from app.core.config import DATA_DIR
from app.service.intent_service import get_prediction
from app.service.training import train_model

router = APIRouter(prefix="/api", tags=["Intent Prediction"])


class QueryRequest(BaseModel):
    query: str

class ModelType(str, Enum):
    catboost = "catboost"
    svm = "svm"

@router.post("/predict")
def predict_intent_route(request: QueryRequest,model: str | None = Query(default=None)):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query must not be empty.")

    try:
        # List valid models from the models directory
        valid_models = [
            d for d in os.listdir("models")
            if os.path.isdir(os.path.join("models", d)) and not d.startswith(".")
        ]

        # If no model is provided, use latest available one
        if model is None:
            if not valid_models:
                raise HTTPException(status_code=404, detail="No models available.")
            model = sorted(valid_models)[-1]

        # Validate that selected model exists
        if model not in valid_models:
            raise HTTPException(status_code=400, detail=f"Invalid model: '{model}'. Choose from: {valid_models}")

        # Proceed with prediction
        intent, answer, confidence = get_prediction(request.query, model)

        return {"intent": intent, "answer": answer, "confidence": round(confidence, 2)}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models")
def list_models():
    model_dir = "models"
    try:
        models = [
            d
            for d in os.listdir(model_dir)
            if os.path.isdir(os.path.join(model_dir, d)) and not d.startswith(".")
        ]
        return {"models": sorted(models)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/train")
async def train_model_route(file: UploadFile = File(...), model_type: ModelType = Form(...)):
    try:
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M")
        directory = DATA_DIR
        os.makedirs(directory, exist_ok=True)

        original_name = Path(file.filename).stem
        extension = Path(file.filename).suffix
        file_location = os.path.join(
            directory, f"{original_name}_{timestamp}{extension}"
        )

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Train the model using the file
        result = train_model(file_location, model_type=model_type.value)

        return {"status": "success", "message": result}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error during model training: {str(e)}"
        )
