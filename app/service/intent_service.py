import os
import joblib
import numpy as np
from sentence_transformers import SentenceTransformer

from app.core.config import INTENT_ANSWER_JSON, MODEL_DIR

embedder = SentenceTransformer("all-mpnet-base-v2")

def get_prediction(query: str, model: str, threshold: float = 0.2):
    threshold = float(threshold)

    model_dir = os.path.join(MODEL_DIR, model)
    if not os.path.isdir(model_dir):
        raise FileNotFoundError(f"Model directory not found: {model_dir}")

    clf = joblib.load(os.path.join(model_dir, "intent_classifier.pkl"))
    label_encoder = joblib.load(os.path.join(model_dir, "label_encoder.pkl"))
    embeddings = embedder.encode([query], normalize_embeddings=True)
    probabilities = clf.predict_proba(embeddings)
    max_prob = float(np.max(probabilities))

    if max_prob >= threshold:
        pred_class_id = clf.classes_[np.argmax(probabilities)]
        intent = label_encoder.inverse_transform([pred_class_id])[0]
    else:
        intent = "unknown_intent"

    answer = INTENT_ANSWER_JSON.get(intent, "No answer found for this intent.")
    return intent, answer, max_prob
