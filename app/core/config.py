import json

MODEL_DIR = "models"
DATA_DIR = "data/uploaded_data/"

with open("data/intent_answers.json", "r", encoding="utf-8") as f:
    INTENT_ANSWER_JSON = json.load(f)
